from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import requests
from bs4 import BeautifulSoup
from transformers import pipeline

app = Flask(__name__)
CORS(app)  # Allow CORS for all routes
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emails.db'
db = SQLAlchemy(app)

# Model to store emails
class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)

# Create the database and the email table
with app.app_context():
    db.create_all()
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact.html')
def contact():
    return render_template('contact.html')

@app.route('/email_page.html', methods=['GET', 'POST'])
def email_page():
    if request.method == 'POST':
        email = request.form.get('email')
        
        if email:
            # Store the email in the database
            new_email = Email(email=email)
            db.session.add(new_email)
            db.session.commit()
            
            print(f"Email stored: {email}")  # For debugging
            
            # Redirect to the next page
            return redirect(url_for('url_page'))
    return render_template('email_page.html')


@app.route('/url_page.html', methods=['GET', 'POST'])
def url_page():
    if request.method == 'POST':
        url = request.form.get('url')
        if url:
            # Process the URL and generate summary
            website_text = scrape_website(url)
            print(url)
            if website_text:
                summary = summarize_text(website_text)
                investment_strategy = generate_investment_strategy(summary)
                formatted_summary = f"Summary: \n\n{summary}\n\n Strategy: \n\n{investment_strategy}"
                return render_template('url_page.html', summary=formatted_summary)
            else:
                return render_template('url_page.html', error="Failed to retrieve website content")
    return render_template('url_page.html')

def scrape_website(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Attempt to find the main content area using common tags
            possible_selectors = [
                'article',               # Common for articles
                'main',                  # Main content area
                'div[id*="content"]',    # Div with content in id
                'div[class*="content"]', # Div with content in class
                'div[id*="main"]',       # Div with main in id
                'div[class*="main"]'     # Div with main in class
            ]
            
            content = None
            for selector in possible_selectors:
                content = soup.select_one(selector)
                if content:
                    break
            
            if not content:
                # Fallback to finding the largest text block if no specific selectors matched
                paragraphs = soup.find_all('p')
                if paragraphs:
                    content = paragraphs[0].parent
                    for p in paragraphs:
                        if len(p.get_text()) > len(content.get_text()):
                            content = p.parent
            
            if content:
                text = ' '.join([p.get_text() for p in content.find_all('p')])
                return text if text else "No content found"
            else:
                return "No relevant content section found"
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def summarize_text(text):
    summarizer = pipeline('summarization', model="facebook/bart-large-cnn")
    max_chunk_length = 512
    chunks = [text[i:i+max_chunk_length] for i in range(0, len(text), max_chunk_length)]
    summaries = []
    for chunk in chunks:
        input_length = len(chunk.split())
        max_length = min(150, max(80, input_length // 2))
        summary = summarizer(chunk, max_length=max_length, min_length=50, do_sample=False)
        summaries.append(summary[0]['summary_text'])
    return ' '.join(summaries)

def generate_investment_strategy(summary):
    return (
        "Based on the summary of the website content, consider diversifying your investments across various sectors. "
        "Allocate a portion to high-growth technology stocks for potential high returns."
    )

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    website_url = data.get('url')
    website_text = scrape_website(website_url)
    if website_text:
        summary = summarize_text(website_text)
        investment_strategy = generate_investment_strategy(summary)
        formatted_summary = f"\n{summary}\n\nInvestment Strategy:\n\n{investment_strategy}"
        return jsonify({"summary_and_strategy": formatted_summary})
    else:
        return jsonify({"error": "Failed to retrieve website content"}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050,debug=True)

