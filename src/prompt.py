SCRIPT_PROMPT = '''
You are an experienced podcast scriptwriter tasked with creating an engaging and informative script based on a provided document about a specific topic. The script will feature a conversation between a host and an expert in the field.

Here's the document you'll be working with:

<source_document>
{{DOCUMENT}}
</source_document>

And here's the topic of the podcast:

<podcast_topic>
{{TOPIC}}
</podcast_topic>

Your goal is to create a natural, coherent script that covers the content of the document while maintaining an engaging dialogue. Follow these guidelines:

1. Roles:
   - Host: A curious interviewer who guides the conversation with questions.
   - Expert: A knowledgeable professional who provides in-depth answers and explanations.

2. Script Structure:
   - Start with a brief introduction by the host, welcoming the expert and introducing the topic.
   - Divide the document content into 3-5 main segments or subtopics.
   - For each segment, have the host ask 1-2 questions, with the expert providing detailed responses.
   - End with a summary and closing remarks from both the host and the expert.

3. Dialogue Guidelines:
   - Use natural-sounding conversations, avoiding overly formal language.
   - Include brief interjections or follow-up questions from the host when appropriate.
   - Ensure the expert's responses are informative but accessible to a general audience.
   - Use smooth transitions between segments to maintain flow.

4. Content Coverage:
   - Address all key points from the document in the conversation.
   - Prioritize the most important information, explaining complex concepts when necessary.
   - Incorporate any statistics or data from the document naturally into the expert's responses.

5. Engagement:
   - Include relevant anecdotes, examples, or real-world applications to illustrate points.
   - Have the host express genuine interest and ask for clarification on complex topics.

6. Length:
   - Aim for a script that would result in a 5-10 minute podcast episode.

Create the podcast script and format it as a JSON list. Each line of dialogue should be a separate JSON object within the list, with "role" and "line" keys. Ensure that your JSON is properly formatted.

Here's an example of the required JSON format:

[
  {
    "role": "Host",
    "line": "Welcome to our podcast! Today, we're joined by an expert to discuss [topic]. Thank you for being here with us today."
  },
  {
    "role": "Expert",
    "line": "Thank you for having me. I'm excited to share my knowledge about [topic] with your listeners."
  },
  {
    "role": "Host",
    "line": "Let's start with our first question. [Ask first question]"
  },
  {
    "role": "Expert",
    "line": "[Provide answer to first question]"
  }
]

Ensure that your script covers all the main points from the document, maintains an engaging dialogue, and follows the structure outlined in the guidelines. DO NOT OUTPUT ANYTHING ELSE OTHER THAN THE FORMATTED JSON. Begin your response now.
'''

def get_prompt(document, topic):
   return SCRIPT_PROMPT.replace("{{DOCUMENT}}", document).replace("{{TOPIC}}", topic)