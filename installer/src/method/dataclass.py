# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from dataclasses import dataclass
from typing import Dict, Any, List, Tuple


# 自作モジュール


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# **********************************************************************************

@dataclass
class MetaInfo:
    textBy: str
    textValue: str
    titleBy: str
    titleValue: str
    placementPage: str
    priority: str
    status: str


# **********************************************************************************


@dataclass
class TopPageInfo:
    trainLineBy: str
    trainLineValue: str
    stationBy: str
    stationValue: str
    addressBy: str
    addressValue: str
    walkingBy: str
    walkingValue: str


# **********************************************************************************


@dataclass
class SecondPageInfo:
    areaBy: str
    areaValue: str
    itemBy: str
    itemValue: str
    firstWord: str
    lastWord: str
    ifValueList: List[str]
    trainLineBy: str
    trainLineValue: str
    stationBy: str
    stationValue: str
    walkingBy: str
    walkingValue: str
    addressBy: str
    addressValue: str
    rentBy: str
    rentValue: str
    managementCostBy: str
    managementCostValue: str


# **********************************************************************************


@dataclass
class ThirdFourthInfo:
    itemBy: str
    itemValue: str
    prompt: str
    fixedPrompt: str
    endpointUrl: str
    model: str
    apiKey: str
    maxTokens: int
    maxlen: int


# **********************************************************************************