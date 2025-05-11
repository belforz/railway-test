import re
import random
import unicodedata
from typing import Optional, Literal

class MessageProcessor:
    COMMON_RESPONSES = {
        r"\b(ola?|olá|ei|e aí)\b": "Olá! Como posso te ajudar com o portfólio? 😊",
        r"\b(tudo\s+bem|como\s+vai|td\s+bem)\b": "Estou bem, obrigado! E você?",
    }

    Section = Literal["experiencias", "projetos", "habilidades", "formacao","certificacoes","idiomas","interesses"]

    SECTION_PATTERNS = {
        "experiencias": [
            r"\b(experiênc(ia|ias)|carreira|trajetóri(a|as)|empregos?|trabalh(a|ou|os|ei))\b",
            r"\b(estágio|empresa(s)?|cliente(s)?|projetos\s+anteriores|função|cargo(s)?)\b"
        ],
        "projetos": [
            r"\b(projetos?|portfolio|case(s)?|desenvolv(eu|endo|er)|implement(a|ei|ou))\b",
            r"\b(app(s)?|aplicaç(ão|ões)|sistema(s)?|soluç(ões|ão)|automação)\b"
        ],
        "habilidades": [
            r"\b(skill(s)?|habilidade(s)?|ferramenta(s)?|tecnolog(ia|ias)|framework(s)?|linguagens?)\b",
            r"\b(stack|domina|usa|trabalha\s+com|conhece)\b",
            r"\b(softskill(s)?)|b(hardskill(s)?)\b"
        ],
        "formacao": [
            r"\b(formaç(ão|ões)|educaç(ão|ões)|gradua(ção|ndo)|cursa|estuda|estudante)\b",
            r"\b(faculdade|universidade|instituição|certificações?|curso(s)?(?! de projeto))\b"
        ],
        "certificacoes": [
    r"\b(certificacoes?|certificados?|de\s+projetos?)\b",
    r"\b(cursos|workshops?|palestras?|eventos?)\b"
],

        "idiomas":[
            r"\b(inglês|espanhol|francês|idiomas?|lingua(s)?|língua(s)?)\b"
        ],
        "interesses":[
            r"\b(interesses?|hobbies?|atividades?\s+extracurriculares?)\b"
        ],
        
    }

    @classmethod
    def process(cls, message: str) -> Optional[str]:
        cleaned = cls._normalize_text(message)

        for pattern, response in cls.COMMON_RESPONSES.items():
            if re.search(pattern, cleaned, re.IGNORECASE):
                return response

        return None 

    @classmethod
    def detect_section(cls, message: str, portfolio_data: dict[str,list[str]]):
        cleaned = cls._normalize_text(message)
        hits = {}
        
        for section, content_list in portfolio_data.items():
            content_text = cls._normalize_text("".join(content_list))
            for word in cleaned.split():
                if word in content_text:
                    hits[section] = hits.get(section,0) + 2

        for section,patterns in cls.SECTION_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, cleaned, re.IGNORECASE):
                    hits[section] = hits.get(section,0) + 1
        return sorted(hits, key=hits.get, reverse=True)       


        

    @staticmethod
    def _normalize_text(text: str) -> str:
        normalized = unicodedata.normalize('NFKD', text.lower())
        return ''.join([c for c in normalized if not unicodedata.combining(c)])
