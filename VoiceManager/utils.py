import csv
import json
import tempfile
from enum import Enum
from json import JSONDecodeError

default_project_settings = {
    "dataBase": {
        "type": "sqlite",
        "path": "",
        "table_name": "ScriptTable",
        "headers": [
            {
                "name": "序号",
                "type": "INTEGER"
            },
            {
                "name": "台词标识名",
                "type": "TEXT PRIMARY KEY NOT NULL"
            },
            {
                "name": "角色",
                "type": "TEXT"
            },
            {
                "name": "台词内容",
                "type": "TEXT"
            },
            {
                "name": "文件名",
                "type": "TEXT"

            },
            {
                "name": "行号",
                "type": "TEXT"
            },
            {
                "name": "RenPy脚本",
                "type": "TEXT"
            },
            {
                "name": "语音文件",
                "type": "BLOB"
            },
            {
                "name": "语音文件格式",
                "type": "TEXT"
            }
        ],
        "VACUUM": True,
        "AUTO_VACUUM": "INCREMENTAL",
    },
    "info": {
        "dataBase": {
            "headers": "do not modifier headers,unless Renpy officially changed the format of the exported dialogue file.",
            "VACUUM": "VACUUM is a command that reclaims unused space in a database file.",
            "AUTO_VACUUM": "AUTO_VACUUM is a pragma that controls the automatic vacuuming of a database file.NONE/FULL/INCREMENTAL"
        }
    }
}


def readTabFile(fileName):
    with open(fileName, 'r', encoding='utf-8') as f:
        cols = [column for column in csv.reader(f, delimiter='\t')]
        headColumn = cols[0]
        dataColumns = cols[1:]

    return headColumn, dataColumns


def loadCharaDefine():
    try:
        with open("chara_define.json", 'r', encoding='utf-8') as f:
            charaDefine = json.load(f)
            charaDefine.pop("_TIME")
            charaDefine = {v: k for k, v in charaDefine.items()}
            print("load chara_define.json success")
    except FileNotFoundError:
        charaDefine = None
    except JSONDecodeError:
        charaDefine = None
    return charaDefine


def translateCharacter(_data: list, charaDefine=None) -> list:
    if charaDefine is None:
        return _data
    else:
        _data[1] = charaDefine.get(_data[1], _data[1])
        if _data[1] == "":
            _data[1] = "旁白"
        return _data


def dumpTempAudio(_audioData, _suffix):
    print("utils", "play_audio")
    f = tempfile.NamedTemporaryFile(mode='wb', suffix=_suffix, dir='', delete=False)
    f.write(_audioData)
    f.close()
    return f.name


def readDBFile(fileName):
    pass


class SearchText:
    class SearchMode(Enum):
        IN = 0
        ALL = 1
        BEGIN_WITH = 2
        END_WITH = 3

    _searchModeTranslation = {
        SearchMode.IN: "匹配部分",
        SearchMode.ALL: "匹配全部",
        SearchMode.BEGIN_WITH: "匹配开头",
        SearchMode.END_WITH: "匹配结尾"
    }

    @classmethod
    def getSearchModeTranslation(cls, mode: SearchMode):
        return cls._searchModeTranslation[mode]

    @classmethod
    def getSearchModeTranslationList(cls):
        return list(cls._searchModeTranslation.values())

    @classmethod
    def getSearchMode(cls, translation: str):
        for key, value in cls._searchModeTranslation.items():
            if value == translation:
                return key
        return None

    @classmethod
    def getSQLLikePattern(cls, text: str, mode: SearchMode):
        if mode == cls.SearchMode.IN:
            return f"%{text}%"
        elif mode == cls.SearchMode.ALL:
            return f"{text}"
        elif mode == cls.SearchMode.BEGIN_WITH:
            return f"{text}%"
        elif mode == cls.SearchMode.END_WITH:
            return f"%{text}"
        else:
            raise ValueError("Unsupported search mode")
