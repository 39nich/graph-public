from openai import OpenAI
import os
from dotenv import load_dotenv
import json
import base64
import re
import mimetypes
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

GRAPH_PROMPT = """
Analyze an image of a graph to extract important information and return it in a structured JSON format.

Instructions:

- Identify and focus on the most prominent graph in the image. The graph may be standalone or embedded in a document.
- Determine the graph type: scatter plot, line graph, or curve.
- Extract the following information:
  - The title of the graph. If title is not visible, put "Not Found".
  - Labels for the x-axis and y-axis, including units if available. If an axis label is not visible, put "Not Found".
  - A detailed natural-language description of the graph's shape, scale of values and trend — sufficient for someone who cannot see it to imagine what it looks like.
  - The description should to interpret the overall meaning of the graph and briefly describe the relationship that it is trying to convey without inferring any unknown information. 
  - Coordinate data:
  - Your goal is to extract coordinate data that can be used to faithfully recreate the shape of the graph on a canvas.
  - For scatter plots and line graphs, return an ordered list of [x, y] points from the most prominent graph. Only include relevant, visible points — avoid duplicate values.
  - For smooth or curved graphs, return a sparse but well-distributed list of points that capture the full curve shape accurately. Prioritize turning points (maxima/minima), inflection points, and representative shape-preserving intervals.
  - Ensure the values reflect the actual graph's axis scale and units. Do not normalize, round off, or interpolate beyond what is visible in the graph.
  - Return the data as a simple list of 2D coordinate pairs, like [[x1, y1], [x2, y2], ...].

Output Format:

Return only a **raw JSON object** in the following format:

{
  "coord_data": [[x1, y1], [x2, y2], ...],
  "graph_type": "Scatter",      // or "Line", "Curve"
  "graph_description": "A detailed description of the graph...",
  "title": "Graph title here",
  "x_label": "X-axis label (with units if any)",
  "y_label": "Y-axis label (with units if any)"
}

Important:

- You must respond strictly with a valid JSON object — no additional commentary, explanations, or markdown formatting.
- Do not wrap the JSON in triple backticks or include any headers.
- The JSON must be parsable with standard tools like `json.loads()`.
- Be as accurate and complete as possible in your analysis and data extraction.
"""
def analyze_image(image_path: str) -> dict:
    mime_type, _ = mimetypes.guess_type(image_path)

    if mime_type not in ["image/png", "image/jpeg"]:
        raise ValueError(f"Unsupported image type: {mime_type}")
    
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")
    
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {
                "role": "system",
                "content": GRAPH_PROMPT.strip()
            }, 
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{base64_image}"
                        }
                    }
                ]
            }], 
        temperature=1,
        max_tokens=2048,
        top_p=1,
    )
    
    # usage = response.usage
    # if usage:
    #     print(f"Tokens used — prompt: {usage.prompt_tokens}, completion: {usage.completion_tokens}, total: {usage.total_tokens}")
    # output = response
    output = response.choices[0].message.content
    if output.strip().startswith("```"):
        output = re.sub(r"^```(?:json)?|```$", "", output.strip(), flags=re.IGNORECASE).strip()
    try:
        result = json.loads(output)
    except json.JSONDecodeError:
        raise ValueError("Model returned invalid JSON:\n" + output)

    return result

        
