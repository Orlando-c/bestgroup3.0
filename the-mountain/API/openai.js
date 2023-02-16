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

// Import required libraries
const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const fetch = require('node-fetch');

// Set up Express server and SQLite database
const app = express();
const port = 3000;
const db = new sqlite3.Database('responses.db');
db.run('CREATE TABLE IF NOT EXISTS responses (id INTEGER PRIMARY KEY AUTOINCREMENT, prompt TEXT, response TEXT)');

// Array of possible prompts
const prompts = [
  'Make a legend!',
  'Make a fable!',
  'Make a short story about an adventure to the peak of a mountain!',
  'Make a short story about an adventure through a forest!',
  'Make a story about a villain!',
  'Make a story about a hero!'
];

// Set up API endpoint to receive a request and generate a response
app.get('/response', (req, res) => {
  // Generate a random index number
  const randomIndex = Math.floor(Math.random() * prompts.length);

  // Use the OpenAI API to send the prompt to the chatbot and receive a response
  const apiKey = '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'; // Replace with your actual API key
  const chatEndpoint = 'https://api.openai.com/v1/engine/text-davinci-003/completions';

  const prompt = prompts[randomIndex];
  const data = {
    'prompt': prompt,
    'max_tokens': 50,
    'temperature': 0.5,
    'n': 1,
    'stop': '\n'
  };

  fetch(chatEndpoint, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${apiKey}`
    },
    body: JSON.stringify(data)
  })
  .then(response => response.json())
  .then(responseData => {
    const responseText = responseData.choices[0].text;

    // Insert the prompt and response into the database
    db.run('INSERT INTO responses (prompt, response) VALUES (?, ?)', [prompt, responseText], function(error) {
      if (error) {
        console.error(error);
      } else {
        console.log(`Saved response for prompt: ${prompt}`);
      }
    });

    // Send the response text to the frontend as HTML
    const html = `<h1>OpenAI Chatbot Response</h1><p><strong>Prompt:</strong> ${prompt}</p><p><strong>Response:</strong> ${responseText}</p>`;
    res.send(html);
  })
  .catch(error => {
    console.error(error);
  });
});

// Start the server
app.listen(port, () => {
  console.log(`Server listening at http://localhost:${port}`);
});