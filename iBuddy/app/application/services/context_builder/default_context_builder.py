from app.domain.entities.search_result import (
    SearchResult,
)
from app.domain.services.context_builder import (
    ContextBuilder,
)

class DefaultContextBuilder(ContextBuilder):

    def build(
            self,
            results: list[SearchResult],
    ) -> str:
        contexts: list[str] = []

        for result in results:
            contexts.append(
                f"""
               <document>
                    <file_name>{result.file_name}</file_name>
                    <chunk_text>
                        {result.chunk_text}
                    </chunk_text>
               </document> 
             """.strip()
            )

        return (
                "<context>\n"
                + "\n\n".join(contexts)
                + "\n</context>"
        )