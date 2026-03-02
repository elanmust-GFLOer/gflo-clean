class FlowkeeperUS:
    def __init__(self, name="Felhasználó"):
        self.name = name
        self.questions = [
            "Mit jelent számodra a szuverenitás?",
            "Milyen kapcsolatban vagy a technológiával?",
            "Mit vársz egy AI partnertől?",
            "Mi a legfontosabb érték számodra?"
        ]
    
    def ask_questions(self):
        print(f"\nÜdv, {self.name}! Kérlek, válaszolj néhány kérdésre:\n")
        answers = {}
        for i, q in enumerate(self.questions, 1):
            print(f"{i}. {q}")
            ans = input("Válasz: ").strip()
            answers[f"q{i}"] = ans
        # Összefoglaló generálása
        summary = f"A felhasználó számára fontos: {answers.get('q1', 'nem adott meg')}. "
        summary += f"Technológiához való viszonya: {answers.get('q2', 'nem adott meg')}. "
        summary += f"AI-val szembeni elvárása: {answers.get('q3', 'nem adott meg')}. "
        summary += f"Legfontosabb értéke: {answers.get('q4', 'nem adott meg')}."
        return {"válaszok": answers, "összefoglaló": summary}
    
    def show_profile(self, profile):
        print("\n=== PROFIL ÖSSZEFOGLALÓ ===")
        print(profile["összefoglaló"])
        print("=============================\n")
