import tkinter as tk
import sqlite3

# --- Database Setup ---
conn = sqlite3.connect("faq.db")
cursor = conn.cursor()

# Create FAQ table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS faq (
    question TEXT,
    answer TEXT
)
""")
conn.commit()

# Sample data (only if table empty)
cursor.execute("SELECT COUNT(*) FROM faq")
if cursor.fetchone()[0] == 0:
    faq_data = [
        ("hello", "Hi there! How can I help you today?"),
        ("pricing", "Our pricing plans start from $9.99/month."),
        ("support", "You can reach support at support@example.com."),
        ("bye", "Goodbye! Have a great day.")
    ]
    cursor.executemany("INSERT INTO faq VALUES (?,?)", faq_data)
    conn.commit()


# --- Bot Logic ---
def get_answer(user_input):
    user_input = user_input.lower()
    cursor.execute("SELECT answer FROM faq WHERE question LIKE ?", ('%' + user_input + '%',))
    result = cursor.fetchone()
    if result:
        return result[0]
    return "Sorry, I don’t understand that yet."


# --- Tkinter UI ---
def send_message():
    user_text = entry.get()
    if not user_text.strip():
        return
    chat_log.config(state=tk.NORMAL)
    chat_log.insert(tk.END, "You: " + user_text + "\n")
    answer = get_answer(user_text)
    chat_log.insert(tk.END, "Bot: " + answer + "\n\n")
    chat_log.config(state=tk.DISABLED)
    entry.delete(0, tk.END)

# Window
root = tk.Tk()
root.title("AI Support Bot")
root.geometry("400x500")

chat_log = tk.Text(root, state=tk.DISABLED, wrap=tk.WORD)
chat_log.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

entry = tk.Entry(root)
entry.pack(padx=10, pady=5, fill=tk.X)

send_btn = tk.Button(root, text="Send", command=send_message)
send_btn.pack(padx=10, pady=5)

root.mainloop()
