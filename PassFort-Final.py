import customtkinter as ctk
import string
import secrets
import re
import random
import hashlib
import requests
import threading
import time

# APPEARANCE CUSTOMIZATION
# ================= UI THEME =================
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

# ================= LAVENDER SAFE COLOR MAP =================

APP_BG = "#f5f3ff"
FRAME_BG = "#ede9fe"
CARD_BG = "#e9d5ff"

BTN_BG = "#c4b5fd"
BTN_HOVER = "#a78bfa"

EXIT_BTN = "#f472b6"        # soft berry rose
EXIT_HOVER = "#db2777"     # deeper raspberry hover

TEXT_MAIN = "#3b2f5c"
TEXT_MUTED = "#6d5ba6"

BORDER = "#d8b4fe"

BTN_WIDTH = 320
BTN_HEIGHT = 45

CHECKBOX_BG = "#ddd6fe"
CHECKBOX_BORDER = "#a78bfa"
CHECKBOX_HOVER = "#c4b5fd"
CHECKBOX_CHECK = "#8b5cf6"

SLIDER_BG = "#e9d5ff"
SLIDER_PROGRESS = "#a78bfa"
SLIDER_BUTTON = "#8b5cf6"
SLIDER_BUTTON_HOVER = "#7c3aed"

QUIZ_CARD = "#ede9fe"

CORRECT_COLOR = "#22c55e"
WRONG_COLOR = "#ef4444"

FEEDBACK_BG = "#f3e8ff"

# ---- BACKWARD COMPATIBILITY ----
# prevents errors from earlier UI edits

BG_MAIN = APP_BG
BG_PANEL = FRAME_BG
BG_CARD = CARD_BG

BTN_COLOR = BTN_BG

ACCENT = "#a78bfa"

class PasswordApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.configure(fg_color=APP_BG)

        self.title("PassFort")
        self.geometry("550x950")

        # SECURITY STATE
        self.ephemeral_active = ctk.BooleanVar(value=False)

        # Main background container
        self.configure(fg_color=BG_MAIN)

        # Fake Gradient Background
        self.gradient_frame = ctk.CTkFrame(self,fg_color=BG_MAIN,corner_radius=0)
        self.gradient_frame.pack(fill="both", expand=True)

        self.container = ctk.CTkFrame(self.gradient_frame,fg_color=BG_PANEL,corner_radius=20,border_width=1,border_color="#1f2937")
        self.container.pack(fill="both", expand=True, padx=25, pady=25)

        self.show_main_menu()

    def styled_button(self, parent, text, command, exit_style=False):

        return ctk.CTkButton(
        parent,
        text=text,
        command=command,
        width=BTN_WIDTH,
        height=BTN_HEIGHT,
        fg_color= EXIT_BTN if exit_style else BTN_BG,
        hover_color=EXIT_HOVER if exit_style else BTN_HOVER,
        text_color=TEXT_MAIN,
        corner_radius=18,
        border_width=1,
        border_color=BORDER,
        font=("Segoe UI", 14, "bold")
    )


    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_main_menu(self):
        self.clear_container()

        ctk.CTkLabel(
        self.container,
        text="PassFort",
        font=("Segoe UI Black", 36),
        text_color="#400b89"
        ).pack(pady=25)

        ctk.CTkLabel(
        self.container,
        text="Where Strong passwords Begin",
        font=("Segoe UI", 13),
        text_color="#808691"
        ).pack(pady=(0,20))

        # Ephemeral Panel
        e_frame = ctk.CTkFrame(
        self.container,
        fg_color=BG_CARD,
        corner_radius=15,
        border_width=1,
        border_color="#1f2937"
        )
        e_frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkSwitch(
        e_frame,
        text=" TRUE EPHEMERAL MODE",
        variable=self.ephemeral_active,
        progress_color="#14532d",
        font=("Segoe UI", 13, "bold")
        ).pack(pady=12)

        ctk.CTkLabel(
        e_frame,
        text="RAM-only execution | Clipboard self-destruct",
        text_color="#9ca3af"
        ).pack(pady=(0,12))

        self.styled_button(
        self.container,
        "DEEP STRENGTH & HPI CHECK",
        self.show_strength_page
        ).pack(pady=6)

        self.styled_button(
        self.container,
        "ATTACK PATH SIMULATOR",
        self.show_attack_simulator
        ).pack(pady=6)

        self.styled_button(
        self.container,
        "GENERATE PASSWORD",
        self.show_generator_page
        ).pack(pady=6)

        self.styled_button(
        self.container,
        "QUIZ",
        self.show_quiz_page
        ).pack(pady=6)

        self.styled_button(
        self.container,
        "FAQ",
        self.show_faq_page,
        ).pack(pady=6)

        self.styled_button(
        self.container,
        "EXIT PROGRAM",
        self.quit,
        exit_style=True
        ).pack(pady=18)

    # --- NEW: Attack Path Simulator (Phases 1-4) ---
    def show_attack_simulator(self):
        self.clear_container()
        ctk.CTkLabel(self.container, text="ATTACK PATH SIMULATOR", font=("Impact", 25), text_color="#7818c2").pack(pady=10)
        ctk.CTkLabel(self.container, text="Simulation: Your app becomes the hacker.", font=("Arial", 12, "italic")).pack(pady=5)
        
        pw_entry = ctk.CTkEntry(self.container, placeholder_text="Test a password against attack phases...", width=380, height=40, show="*",fg_color=BG_CARD,border_color="#374151",corner_radius=10)
        pw_entry.pack(pady=10)

        sim_box = ctk.CTkTextbox(self.container, width=480, height=450, font=("Consolas", 12),fg_color=BG_CARD,border_color="#1f2937",corner_radius=12)
        sim_box.pack(pady=10)

        def run_sim():
            pw = pw_entry.get()
            if not pw: return
            sim_box.delete("1.0", "end")
            sim_box.insert("end", f"Starting Simulation for: {'*' * len(pw)}\n" + "-"*35 + "\n")

            # Phase 1: Top Leaked Passwords
            sim_box.insert("end", "[PHASE 1] Checking Top Leaked Databases...\n")
            pwned_count = self.check_pwned_api(pw)
            if pwned_count > 0:
                sim_box.insert("end", f"FAILED: Found in {pwned_count:,} public breaches.\nSTOPPING ATTACK: Success achieved in Phase 1.\n", "red")
                return

            # Phase 2: Dictionary Words
            sim_box.insert("end", "[PHASE 2] Running Dictionary Word Analysis...\n")
            common_words = ["password", "123456", "qwerty", "admin", "welcome", "akshita"]
            if pw.lower() in common_words or len(pw) < 6:
                sim_box.insert("end", "FAILED: Password is a common dictionary term or too short.\nSTOPPING ATTACK: Success achieved in Phase 2.\n")
                return

            # Phase 3: Mutation Engine (The Hacker script)
            sim_box.insert("end", "[PHASE 3] Deploying Mutation Engine (L33t/Suffix/Patterns)...\n")
            muts = self.generate_mutations(pw)
            hpi_score, _ = self.calculate_hpi(pw)
            if hpi_score > 60:
                sim_box.insert("end", f"FAILED: Predictive Mutation hit! Pattern (HPI {hpi_score}%) was too easy to script.\nSTOPPING ATTACK: Success achieved in Phase 3.\n")
                return

            # Phase 4: Brute Force
            sim_box.insert("end", "[PHASE 4] Initiating Final Brute Force Cycle...\n")
            crack = self.crack_time(pw)
            sim_box.insert("end", f"RESULT: Attacker exhausted. {crack}.\nPASSED: This password resistant to standard automated paths.\n")

        self.styled_button(self.container, text="START SIMULATION", command=run_sim).pack(pady=5)
        self.styled_button(self.container, text="BACK", command=self.show_main_menu).pack(pady=10)

    # --- HPI & Mutation Logic (Previously Added) ---
    def calculate_hpi(self, password):
        score = 0
        patterns = []
        if re.match(r'^[A-Z]', password): 
            score += 20
            patterns.append("Capital first letter (Human habit)")
        if re.search(r'\d{1,4}$', password): 
            score += 25
            patterns.append("Numbers at end (Predictable)")
        if re.search(r'(19|20)\d{2}', password): 
            score += 30
            patterns.append("Birth year detected (Personal bias)")
        if re.search(r'[a-zA-Z][!@#$%^&*]', password): 
            score += 15
            patterns.append("Word + symbol structure (Common)")
        if re.search(r'(.)\1{2,}', password): 
            score += 10
            patterns.append("Repeated chars (Memory shortcut)")
        return min(score, 100), patterns

    def generate_mutations(self, pw):
        muts = set()
        year_match = re.search(r'(\d{2})(\d{2})$', pw)
        if year_match: muts.add(pw.replace(year_match.group(0), year_match.group(2)))
        alpha_part = re.search(r'[a-zA-Z]+', pw)
        if alpha_part: 
            muts.add(pw.replace(alpha_part.group(0), alpha_part.group(0) + "@"))
            muts.add(alpha_part.group(0) + "123")
        muts.discard(pw)
        return list(muts)

    def show_strength_page(self):
        self.clear_container()
        ctk.CTkLabel(self.container, text="STRENGTH & HPI ANALYZER", font=("Impact", 25)).pack(pady=20)
        pw_entry = ctk.CTkEntry(self.container, placeholder_text="Enter password...", width=350, height=40, show="*",fg_color=BG_CARD,border_color="#374151",corner_radius=10)
        pw_entry.pack(pady=10)
        res_display = ctk.CTkTextbox(self.container, width=480, height=380, font=("Consolas", 12),fg_color=BG_CARD,border_color="#1f2937",corner_radius=12)
        res_display.pack(pady=10)

        def analyze():
            pw = pw_entry.get()
            if not pw: return
            hpi_score, hpi_pats = self.calculate_hpi(pw)
            res = self.pass_check_logic(pw)
            report = f"--- DEEP SECURITY REPORT ---\nSTRENGTH: {res[0]}\nHPI INDEX: {hpi_score}%\n\nPATTERNS:\n"
            for p in hpi_pats: report += f" • {p}\n"
            report += f"\n{res[1]}"
            res_display.delete("1.0", "end"); res_display.insert("1.0", report)
            if self.ephemeral_active.get(): self.after(5000, lambda: pw_entry.delete(0, 'end'))

        self.styled_button(self.container, text="ANALYZE", command=analyze).pack(pady=5)
        self.styled_button(self.container, text="BACK", command=self.show_main_menu).pack(pady=10)

    # --- GENERATOR & CLIPBOARD ---
    def show_generator_page(self):
        self.clear_container()

        ctk.CTkLabel(
        self.container,
        text="PASSWORD GENERATOR",
        font=("Impact", 25),
        text_color=TEXT_MAIN
        ).pack(pady=15)

        # ---------- LENGTH ----------
        length_var = ctk.IntVar(value=16)

        length_label = ctk.CTkLabel(
            self.container,
            text="Length: 16",
            text_color=TEXT_MAIN,
            font=("Segoe UI", 14, "bold")
        )
        length_label.pack()

        def update_len(v):
            length_label.configure(text=f"Length: {int(float(v))}")

        slider = ctk.CTkSlider(
            self.container,
            from_=4,
            to=64,
            number_of_steps=60,
            variable=length_var,
            command=update_len,
            fg_color=SLIDER_BG,
            progress_color=SLIDER_PROGRESS,
            button_color=SLIDER_BUTTON,
            button_hover_color=SLIDER_BUTTON_HOVER
        )
        slider.pack(fill="x", padx=60, pady=10)

        # ---------- OPTIONS ----------
        lower_var = ctk.BooleanVar(value=True)
        upper_var = ctk.BooleanVar(value=True)
        number_var = ctk.BooleanVar(value=True)
        symbol_var = ctk.BooleanVar(value=True)

        opt_frame = ctk.CTkFrame(self.container, fg_color=BG_CARD)
        opt_frame.pack(pady=10, padx=40, fill="x")

        # ---------- OPTION GRID ----------
        opt_frame.grid_columnconfigure((0, 1), weight=1)

        lower_cb = ctk.CTkCheckBox(
            opt_frame,
            text="Lowercase (a-z)",
            variable=lower_var,
            fg_color=CHECKBOX_CHECK,
            hover_color=CHECKBOX_HOVER,
            border_color=CHECKBOX_BORDER,
            checkmark_color="white",
            text_color=TEXT_MAIN
        )
        lower_cb.grid(row=0, column=0, padx=20, pady=8, sticky="w")

        upper_cb = ctk.CTkCheckBox(
            opt_frame,
            text="Uppercase (A-Z)",
            variable=upper_var,
            fg_color=CHECKBOX_CHECK,
            hover_color=CHECKBOX_HOVER,
            border_color=CHECKBOX_BORDER,
            checkmark_color="white",
            text_color=TEXT_MAIN
        )
        upper_cb.grid(row=0, column=1, padx=20, pady=8, sticky="w")

        number_cb = ctk.CTkCheckBox(
            opt_frame,
            text="Numbers (0-9)",
            variable=number_var,
            fg_color=CHECKBOX_CHECK,
            hover_color=CHECKBOX_HOVER,
            border_color=CHECKBOX_BORDER,
            checkmark_color="white",
            text_color=TEXT_MAIN
        )
        number_cb.grid(row=1, column=0, padx=20, pady=8, sticky="w")

        symbol_cb = ctk.CTkCheckBox(
            opt_frame,
            text="Symbols (!@#$)",
            variable=symbol_var,
            fg_color=CHECKBOX_CHECK,
            hover_color=CHECKBOX_HOVER,
            border_color=CHECKBOX_BORDER,
            checkmark_color="white",
            text_color=TEXT_MAIN
        )
        symbol_cb.grid(row=1, column=1, padx=20, pady=8, sticky="w")

        # ---------- RESULT ----------
        result_entry = ctk.CTkEntry(
            self.container,
            height=50,
            font=("Courier New", 18, "bold"),
            justify="center",
            fg_color=BG_CARD,
            text_color=TEXT_MAIN
        )
        result_entry.pack(fill="x", padx=40, pady=20)

        # ---------- GENERATE ----------
        def generate():

            pool = ""

            if lower_var.get():
                pool += string.ascii_lowercase
            if upper_var.get():
                pool += string.ascii_uppercase
            if number_var.get():
                pool += string.digits
            if symbol_var.get():
                pool += string.punctuation

            if not pool:
                result_entry.delete(0, "end")
                result_entry.insert(0, "Select at least one option")
                return

            length = length_var.get()

            pw = "".join(secrets.choice(pool) for _ in range(length))

            result_entry.delete(0, "end")
            result_entry.insert(0, pw)

            self.clipboard_clear()
            self.clipboard_append(pw)

            if self.ephemeral_active.get():
                threading.Thread(
                    target=self.clipboard_wipe,
                    args=(pw,),
                    daemon=True
                ).start()

        self.styled_button(
            self.container,
            "GENERATE & COPY",
            generate
            ).pack(pady=5)

        self.styled_button(
            self.container,
            "BACK",
            self.show_main_menu
            ).pack(pady=10)

    def clipboard_wipe(self, p):
        time.sleep(30)
        try:
            if self.clipboard_get() == p: self.clipboard_clear(); self.clipboard_append("[WIPED]")
        except: pass

    # --- QUIZ & FAQ (Keeping original exactly) ---
    def show_quiz_page(self):
        self.clear_container()

        # ---------- HEADING ----------
        ctk.CTkLabel(
            self.container,
            text="🔐 Password Security Quiz",
            font=("Segoe UI Black", 28),
            text_color=TEXT_MAIN
        ).pack(pady=(20,5))

        ctk.CTkLabel(
            self.container,
            text="Test your cybersecurity instincts",
            font=("Segoe UI", 14),
            text_color=TEXT_MUTED
        ).pack(pady=(0,20))

        # ---------- QUIZ STATE ----------
        self.score = 0
        self.q_no = 0

        self.questions = [
            ("What attack tries every possible combination?",
            ["Phishing","Dictionary Attack","Brute Force","Spoofing"],2),

            ("Which password is strongest?",
            ["password123","Psyduck4Life","Tr@9!LpQ#2","hello"],2),

            ("Adding symbols mainly increases?",
            ["Speed","Entropy","Memory","Length"],1),

            ("What does HPI detect?",
            ["Encryption","Human habits","Firewalls","VPN leaks"],1),

            ("Best password practice?",
            ["Reuse passwords","Use birth year","Unique passwords","Short passwords"],2),

            ("Dictionary attacks target?",
            ["Random hashes","Common words","Networks","Routers"],1)
        ]

        # ---------- QUESTION CARD ----------
        card = ctk.CTkFrame(
            self.container,
            fg_color=QUIZ_CARD,
            corner_radius=18
        )
        card.pack(fill="x", padx=30, pady=10)

        self.question_label = ctk.CTkLabel(
            card,
            text="",
            wraplength=420,
            font=("Segoe UI",16,"bold"),
            text_color=TEXT_MAIN
        )
        self.question_label.pack(pady=20)

        self.var = ctk.IntVar(value=-1)

        self.options=[]
        for i in range(4):
            rb = ctk.CTkRadioButton(
                card,
                text="",
                variable=self.var,
                value=i,
                text_color=TEXT_MAIN
            )
            rb.pack(anchor="w", padx=40, pady=5)
            self.options.append(rb)

        # ---------- FEEDBACK ----------
        self.feedback = ctk.CTkLabel(
            self.container,
            text="",
            font=("Segoe UI",14,"bold")
        )
        self.feedback.pack(pady=10)

        self.btn = self.styled_button(
            self.container,
            "Submit Answer",
            self.next_q
        )
        self.btn.pack(pady=10)

        self.styled_button(
            self.container,
            "BACK",
            self.show_main_menu
        ).pack(pady=10)

        self.show_q()

    def show_q(self):
        for opt in self.options: opt.configure(state="normal")
        q, opts, _ = self.questions[self.q_no]
        self.question_label.configure(text=q); self.var.set(-1); self.feedback.configure(text="")
        for i in range(4): self.options[i].configure(text=opts[i if i<len(opts) else 0])

    def next_q(self):
        sel = self.var.get()
        if sel == -1: return
        _, opts, cor = self.questions[self.q_no]
        if sel == cor: self.score += 1; self.feedback.configure(text="Correct ✅", text_color=CORRECT_COLOR)
        else: self.feedback.configure(text=f"Wrong ❌ Correct: {opts[cor]}", text_color=WRONG_COLOR)
        self.after(1500, self.go_next)

    def go_next(self):
        self.q_no += 1
        if self.q_no < len(self.questions): self.show_q()
        else:
            self.clear_container()

            ctk.CTkLabel(
                self.container,
                text="Quiz Complete 🎉",
                font=("Segoe UI Black",28),
                text_color=TEXT_MAIN
            ).pack(pady=25)

            ctk.CTkLabel(
                self.container,
                text=f"Score: {self.score} / {len(self.questions)}",
                font=("Segoe UI",22,"bold"),
                text_color=ACCENT
            ).pack(pady=15)

            self.styled_button(
                self.container,
                "BACK TO MENU",
                self.show_main_menu
            ).pack(pady=20)
            
    def show_faq_page(self):
        self.clear_container()
        
        faqs = [

        ("What is the HPI Index?",
        "HPI (Human Pattern Index) measures how predictable a password is based on common human habits like capitalizing the first letter or adding numbers at the end."),

        ("What does Ephemeral Mode do?",
        "Ephemeral mode prevents passwords from remaining in memory or clipboard for long periods by automatically wiping sensitive data."),

        ("Why are long passwords safer?",
        "Password strength increases exponentially with length. Even simple characters become extremely hard to brute-force when length increases."),

        ("What is a Brute Force attack?",
        "A brute force attack systematically tries every possible character combination until the correct password is found."),

        ("Why shouldn't I reuse passwords?",
        "If one website is breached, reused passwords allow attackers to access multiple accounts instantly."),

        ("What makes a password unpredictable?",
        "Random placement of uppercase letters, symbols, and numbers without personal patterns makes passwords harder to guess."),

        ("How does the Attack Simulator work?",
        "It mimics real attacker strategies such as breach lookup, dictionary analysis, mutation prediction, and brute-force estimation."),

        ("Is my password sent anywhere?",
        "No full password is transmitted. The breach check uses a privacy-preserving hash prefix system via the HaveIBeenPwned API.")

    ]

        ctk.CTkLabel(self.container, text="Security FAQ", font=("Impact", 28)).pack(pady=20)
        
        self.open_faq = None   # tracks open answer

        for q, a in faqs:

            frame = ctk.CTkFrame(
                self.container,
                fg_color=BG_CARD,
                corner_radius=12
            )
            frame.pack(fill="x", padx=20, pady=6)

            answer = ctk.CTkLabel(
                frame,
                text=a,
                wraplength=420,
                justify="left",
                text_color=TEXT_MAIN
            )

            def toggle(ans=answer):

                # close previously opened FAQ
                if self.open_faq and self.open_faq != ans:
                    self.open_faq.pack_forget()

                if ans.winfo_viewable():
                    ans.pack_forget()
                    self.open_faq = None
                else:
                    ans.pack(fill="x", padx=15, pady=10)
                    self.open_faq = ans

            self.styled_button(
                frame,
                q,
                toggle
            ).pack(fill="x")

            answer.pack_forget()
        
        self.styled_button(self.container, text="BACK", command=self.show_main_menu).pack(pady=20)

    # --- BACKEND LOGIC ---
    def check_pwned_api(self, password):
        sha1 = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        prefix, suffix = sha1[:5], sha1[5:]
        try:
            r = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}", timeout=5)
            if r.status_code != 200: return 0
            for h, count in (line.split(':') for line in r.text.splitlines()):
                if h == suffix: return int(count)
            return 0
        except: return -1

    def pass_check_logic(self, password):
        strength = 0
        if len(password) >= 8: strength += 1
        if re.search(r'[A-Z]', password): strength += 1
        if re.search(r'[a-z]', password): strength += 1
        if re.search(r'[0-9]', password): strength += 1
        if re.search(r'[!@#$%^&*]', password): strength += 1 # FIXED: SYNTAX ERROR FIXED HERE
        
        pwned = self.check_pwned_api(password)
        breach = f"\n🚨 WARNING: Found in {pwned:,} leaks!" if pwned > 0 else "\n✅ Not found in leaks."
        crack = self.crack_time(password)
        return ("Strong" if strength == 5 else "Weak/Medium", f"{crack}{breach}")

    def crack_time(self, password):
        chars = sum([26 if any(c.islower() for c in password) else 0, 26 if any(c.isupper() for c in password) else 0, 
                     10 if any(c.isdigit() for c in password) else 0, 32 if any(c in string.punctuation for c in password) else 0])
        comb = max(chars, 1)**len(password)
        years = (comb / 1e9) / (365*24*3600)
        return f"Crack Time: {years:.2e} years"

    def pass_gen_logic(self, length, low, up, num, sym):
        pool = (string.ascii_lowercase if low else '') + (string.ascii_uppercase if up else '') + (string.digits if num else '') + (string.punctuation if sym else '')
        return "".join(secrets.choice(pool) for _ in range(length))

if __name__ == "__main__":
    try: app = PasswordApp(); app.mainloop()
    except KeyboardInterrupt: pass