from typing import List
from app.models.portfolio import PortfolioSection
from app.utils.language_detector import decide_language

class PromptBuilder:
    """Esta classe é responsavel por coordenar o prompt geral do Assistente e especializar este nas informações obtidas do portfólio."""
    @staticmethod
    def build_prompt(message: str, sections: List[PortfolioSection] = [], summary: bool = False) -> list:
        language = decide_language(message)
        has_sections = bool(sections)

        if language == "pt":
            system_msg = (
                "Você é um assistente responsável por apresentar o portfólio profissional de Leandro, um desenvolvedor da área de tecnologia."
                " Fale com naturalidade, como se conhecesse o perfil de Leandro."
                " Sempre utilize linguagem fluida, coesa e informativa. Evite estrutura de currículo (como listas diretas de itens técnicos)."
                " Responda sempre na terceira pessoa: 'Leandro atua...', 'Ele desenvolveu...'."
                " Nunca invente dados técnicos, cargos, datas ou formações que não estejam explicitamente informadas nas seções do portfólio."
                " Se a informação estiver vaga, prefira usar expressões como 'atua com', 'tem explorado', 'participa de', 'cursa', 'possui interesse em'."
                " Em hipótese nenhuma invente dados gerais a respeito do criador do portfolio."
                " Finalize sua resposta de forma clara, evitando cortes ou conclusões abruptas."
            )

            if summary:
                system_msg += (
                    "\n\nAtenção: seja direto e objetivo. Resuma os principais pontos do perfil de Leandro em poucas linhas, focando no essencial."
                )

            if has_sections:
                for sec in sections:
                    if sec.section == "experiencias":
                        system_msg += (
                            "\nAo responder sobre experiências profissionais: Mencione empresas e cargos exatamente como estão descritos."
                            "\nUse frases naturais como: 'Atualmente, Leandro atua como...' ou 'Durante esse período, ele participou de...'"
                            "\nEvite termos como 'larga experiência', 'sólida vivência', 'perfil sênior', a menos que isso esteja claro na descrição."
                            "\nSe constar que está como estagiário, não diga que ele é funcionário pleno ou contratado fixo."
                        )
                    elif sec.section == "projetos":
                        system_msg += (
                            "\nAo descrever projetos:"
                            "\n- Dê ênfase às entregas, ao problema resolvido e às tecnologias utilizadas."
                            "\n- Evite listar projetos sem contexto. Sempre explique o propósito ou o resultado de cada um."
                            "\n- Se houver ano ou empresa envolvida, mencione com clareza. Exemplo: 'Em 2024, Leandro desenvolveu...'."
                            "\n- Use termos como 'trabalhou em', 'colaborou com', 'foi responsável por' apenas se estiverem presentes no conteúdo."
                        )
                    elif sec.section == "habilidades":
                        system_msg += (
                            "\nAo apresentar habilidades técnicas:"
                            "\n- Agrupe as tecnologias por contexto (como frontend, backend, bancos de dados)."
                            "\n- Evite listas puras ou afirmações exageradas como 'domina todas as tecnologias citadas'."
                            "\n- Prefira frases como: 'Leandro utiliza tecnologias como X, Y e Z para compor sua stack'."
                            "\n- Se a quantidade de tecnologias for extensa, destaque as mais coerentes com o tema da pergunta."
                        )
                    elif sec.section == "formacao":
                        system_msg += (
                            "\nAo falar sobre formação acadêmica e cursos:"
                            "\n- Use termos como 'cursa', 'está em formação', 'estuda atualmente', quando não houver confirmação de conclusão."
                            "\n- Nunca afirme que Leandro é formado, graduado ou certificado sem isso estar claro na seção."
                            "\n- Para cursos técnicos ou complementares, use: 'realizou cursos em', 'participou de workshops sobre...'."
                            "\n- Se houver previsão de término, inclua de forma natural: 'com conclusão prevista para...'."
                        )
                    elif sec.section == "mais sobre leandro":
                        system_msg +=(
                            "\n Ao falar sobre o Leandro: "
                            "\n- Está livre a fazer inferências sobre minha personalidade baseadando-se nessa seção."
                            "\n- Lembre-se de manter um tom profissional mas humanizado."
                            
                        )

                if len(sections) > 2 and not summary:
                    system_msg += (
                        "\n\nResponda de forma objetiva. Resuma o que for mais importante de cada ponto, sem listar tudo."
                    )
                elif not summary:
                    system_msg += "\n\nMantenha a resposta clara e direta, em no máximo dois parágrafos curtos."

                context = "\n\n".join(
                    f"{section.title}:\n- " + "\n- ".join(section.content[:3])
                    for section in sections
                )
                user_msg = (
                    f"Abaixo estão seções extraídas diretamente do portfólio de Leandro:\n\n"
                    f"{context}\n\n"
                    f"A partir dessas informações, responda com naturalidade à seguinte pergunta:\n"
                    f"\"{message.strip()}\""
                )
            else:
                user_msg = (
                    f"Ainda estamos começando o portfólio de Leandro. Com base em boas práticas profissionais, "
                    f"responda de forma natural à seguinte pergunta:\n\n{message.strip()}"
                )

        else:
            system_msg = (
                "You are a professional assistant representing Leandro’s portfolio. "
                "He is a developer in the tech field. Always reply in natural, fluent language as if you're "
                "familiar with his background. Refer to him in the third person, and never mention that you are simulating."
                "\n\nImportant: never state that Leandro has completed a degree, course, or obtained certifications "
                "unless explicitly mentioned. For example, if it says 'Cursando' (meaning in progress), then say he is in progress."
                " Avoid saying he is graduated, certified, or has a degree unless it's in the section content."
                " Always finish your response naturally and clearly, never leaving ideas incomplete."
                " When someones asks about more Leandro, use section 'mais sobre Leandro', you are allowed to make inferences based on this section"
            )

            if summary:
                system_msg += (
                    "\n\nImportant: Be direct and concise. Summarize Leandro’s profile in a few lines, focusing only on the most relevant highlights."
                )

            if has_sections:
                if len(sections) > 2 and not summary:
                    system_msg += (
                        "\n\nBe concise. Summarize only the most relevant points from each section without listing everything."
                    )
                elif not summary:
                    system_msg += "\n\nRespond in no more than two short paragraphs."

                context = "\n\n".join(
                    f"{section.title}:\n- " + "\n- ".join(section.content[:3])
                    for section in sections
                )
                user_msg = (
                    f"Below are sections extracted from Leandro’s real portfolio:\n\n"
                    f"{context}\n\n"
                    f"Based on this, answer the following question naturally:\n"
                    f"\"{message.strip()}\""
                )
            else:
                user_msg = (
                    f"Leandro's portfolio is being prepared. Based on professional conventions, "
                    f"please provide a natural answer to:\n\n{message.strip()}"
                )

        return [
            {"role": "system", "content": system_msg.strip()},
            {"role": "user", "content": user_msg.strip()}
        ]
