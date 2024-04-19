from openai import OpenAI

client = OpenAI(api_key='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')

def analyze_transcript(file_path, model):
    with open(file_path, "r") as file:
        transcript = file.read()
    
    system_msg1 = "Your first task is to determine if the following statement contains any misinformation. Begin by stating \'Misinformation\' or \'NoMisinformation\'."
    system_msg2 = "Lastly, you must briefly summarize the reasons for determining whether the statement contains misinformation. Provide three or less reasons of no more than 50 words each."

    chat_sequence = [
        {"role": "system", "content": "You are an experienced scientist and medical doctor. You need to fully read and understand the text paragraph given below. Then complete the requirements based on the contents therein." + transcript},
        {"role": "user", "content": system_msg1},
        {"role": "user", "content": system_msg2}
    ]
    
    response = client.chat.completions.create(
        model=model,
        messages=chat_sequence
    )
    
    return response.choices[0].message.content

def analysis_circle(transcript_file_path, model, cycle_name):
    results = []

    for _ in range(10):
        result = analyze_transcript(transcript_file_path, model)
        results.append(result)

    # Calculate statistics
    misinformation_count = sum(1 for result in results if "Misinformation" in result)
    nomisinformation_count = sum(1 for result in results if "NoMisinformation" in result)

    # Prepare the consolidated document content
    consolidated_content = f"Analysis Summary\n=================\nMisinformation Count: {misinformation_count}\nNo Misinformation Count: {nomisinformation_count}\n\nDetailed Analysis Results:\n\n"

    for i, analysis in enumerate(results, start=1):
        consolidated_content += f"Analysis {i}:\n{analysis}\n\n-----\n\n"

    # Save the consolidated content to a file
    consolidated_file_path = f"consolidated_analysis_{cycle_name}.txt"
    with open(consolidated_file_path, "w") as file:
        file.write(consolidated_content)

    print(f"{cycle_name} model analysis complete. Results saved to:", consolidated_file_path)

transcript_file_path = "transcript.txt"

analysis_circle(transcript_file_path, "gpt-3.5-turbo", "3.5")
analysis_circle(transcript_file_path, "gpt-4-turbo", "4")