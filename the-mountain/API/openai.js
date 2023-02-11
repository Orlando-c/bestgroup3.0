$.ajax({
    type: 'POST',
    url: 'https://api.openai.com/v1/engines/text-davinci-002/jobs',
    headers: {
      'Authorization': 'Bearer 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',
      'Content-Type': 'application/json'
    },
    data: JSON.stringify({
      'prompt': 'What is your favorite movie?',
      'max_tokens': 100,
      'temperature': 0.5
    }),
    success: function(data) {
      $('#response').text(data.choices[0].text);
    }
  });