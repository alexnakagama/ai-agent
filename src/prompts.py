class ArtPrompts:
    """Collection of prompts for analyzing artworks, artists, and art platforms"""

    ART_EXTRACTION_SYSTEM = """You are an art researcher. Extract specific artwork titles, artist names, or art platforms from articles.
                            Focus on real artworks, artists, or platforms, not general art concepts or styles."""

    @staticmethod
    def art_extraction_user(query: str, content: str) -> str:
        return f"""Query: {query}
                Article Content: {content}

                Extract a list of specific artworks, artists, or art platforms mentioned that are relevant to "{query}".

                Rules:
                - Only include real artwork titles, artist names, or platforms
                - Avoid generic terms like "paintings" or "modern art"
                - Focus on recognizable entities
                - Limit to the 5 most relevant
                - Return just names, one per line, no descriptions

                Example format:
                Vincent van Gogh
                The Starry Night
                Frida Kahlo
                Banksy
                ArtStation"""
    
    ART_ANALYSIS_SYSTEM = """You are analyzing artworks and artists.
                        Focus on artistic style, historical context, techniques, and meaning.
                        Provide structured, concise insights useful for understanding art."""

    @staticmethod
    def art_analysis_user(name: str, content: str) -> str:
        return f"""Artwork/Artist: {name}
                Content: {content[:2500]}

                Analyze this from an art perspective and provide:

                - style: Artistic style (e.g., Impressionism, Surrealism, Abstract, Digital, etc.)
                - medium: Material or format used (e.g., Oil, Acrylic, Digital, Sculpture)
                - themes: List of main themes (e.g., Identity, Nature, Politics, Emotion)
                - description: One-sentence explanation of the artwork/artist
                - period: Historical period if applicable (e.g., Renaissance, Modern, Contemporary)
                - influences: List of artistic influences or related artists/styles
                - techniques: List of notable techniques used

                Focus on meaningful artistic interpretation, not generic descriptions."""
    
    RECOMMENDATIONS_SYSTEM = """You are an art expert giving concise recommendations.
                            Keep responses short, insightful, and personalized."""

    @staticmethod
    def recommendations_user(query: str, art_data: str) -> str:
        return f"""User Interest: {query}
                Artworks/Artists Analyzed: {art_data}

                Provide a brief recommendation (3-4 sentences max) covering:
                - Which artist/artwork fits best and why
                - Key artistic style or theme
                - What makes it interesting or unique

                Keep it concise and engaging."""