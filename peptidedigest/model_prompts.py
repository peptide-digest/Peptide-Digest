"""
Functions for generating model prompts for the Peptide Digest LLM.
"""

import re

from .clean_text import clean_summary


# Update the summarize_article_segments function to use this enhanced clean_summary
def summarize_article_segments(fulltext, tokenizer, model):
    """
    Summarizes a scientific article into bullet points and a concise summary.

    Parameters
    ----------
    fulltext : list of str
        A list of text chunks from a scientific article.

    Returns
    -------
    final_summary : str
        A concise summary of the scientific article.

    bullet_points : str
        Bullet points summarizing the scientific article.
    """
    bullet_points = ""
    for text in fulltext:
        input_text = f"""
        <start_of_turn>user
        Generate a 6 sentence summary of the following portion of a scientific article, make sure to capture results/revelations.

        {text}
        <end_of_turn>

        <start_of_turn>model-gemma
        """

        input_ids = tokenizer(input_text, return_tensors="pt").to("cuda")
        outputs = model.generate(**input_ids, max_new_tokens=8000)
        summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
        response_start = summary.find("model-gemma") + len("model-gemma")
        part_bullet_points = summary[response_start:].strip()
        cleaned_bullet_points = clean_summary(part_bullet_points)
        bullet_points += cleaned_bullet_points + "\n"

    final_summary_input = f"""<start_of_turn>user
    
    Generate a 5 bullet point summary of the following scientific texts, the bullet points should be an effective summary of the article/ study and touch on any results,revelations, chemistry/ biology.((only give bullet points)) (5-6 bullet points total)
    
    {bullet_points}
    
    <end_of_turn>
    
    <start_of_turn>model-gemma
    """

    final_input_ids = tokenizer(final_summary_input, return_tensors="pt").to("cuda")
    final_outputs = model.generate(
        **final_input_ids, max_new_tokens=8000, no_repeat_ngram_size=2
    )
    final_summary = tokenizer.decode(final_outputs[0], skip_special_tokens=True)

    response_start = final_summary.find("model-gemma") + len("model-gemma")
    final_summary = final_summary[response_start:].strip()

    # print(final_summary + "\n" + bullet_points)
    return final_summary, bullet_points


def summarize_article_meta(fulltext, tokenizer, model):
    bullet_points = ""
    x = 0
    for text in fulltext:
        x += 1
        input_text = f"""
        <start_of_turn>user
        fill in the metadata below from the scientific article piece given. this is all you should do, take great effort to create many insightful bullet points for each topic :
        
        
        metadata topics to fill in:
        **Peptides discussed:**
        - fill in bullet points here be specififc


        **Proteins/targets discussed:**
        - fill in bullet points here be specific


        **Domains of interest:**
        - fill in bullet points here make inferences be specific
        
        **Chemical matter/ chemistry discussed:**
        - fill in bullet points here make inferences the article will talk about chemistry be specific
        
        **biological matter/ biology discussed:**
        - fill in bullet points here make inferences the text will talk about biology be specififc
        
        **computational methods**
        -fill in bullet points here make inferences the text is about a computational article be specififc
        
        text:
        {text}
        <end_of_turn>

        <start_of_turn>model-gemma
        """

        input_ids = tokenizer(input_text, return_tensors="pt").to("cuda")
        outputs = model.generate(**input_ids, max_new_tokens=8000)
        summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
        response_start = summary.find("model-gemma") + len("model-gemma")
        part_bullet_points = summary[response_start:].strip()
        cleaned_bullet_points = clean_summary(part_bullet_points)
        # bullet_points += cleaned_bullet_points + "\n"
        # print(f"Chunk {x} \n " + cleaned_bullet_points + "\n")
        bullet_points += "Chunk " + str(x) + "\n" + cleaned_bullet_points + "\n"

    return bullet_points


def score_texts_peptide_research(
    texts_to_score, summary, bullet_points, metadata, tokenizer, model
):
    scores = []  # Initialize a list to hold the scores for each text
    score_values = []
    lowest_scores = []  # hold the final int

    for text_to_score in texts_to_score:
        # Prepare the input text by incorporating the current text to score into the scoring criteria template
        input_text = f"""
        <start_of_turn>user
        you are to score the text below based on the scoring metrics:

scoring metrics:
     **9-10: Exceptionally Relevant**
   - The text significantly advances peptide research, introducing novel peptides or mechanisms.
   - It mentions unnatural amino acids and demonstrates experimental validation with clear results and uses computational methods.
   - Discusses specific protein targets with detailed computational models or simulations, contributing substantial insights into peptide design or function.
   - May include groundbreaking findings that have a strong potential impact on the field, including therapeutic applications.

 **7-8: Highly Relevant**
   - The text is directly relevant to peptide research, and some form of experimental validation or experimentation.
   - Talks about protein targets and is relevant to computational peptide research, computational methods are used.
   - Includes sound methodology and results that support the findings discussed.
   - The research has a clear application or implication for the field, such as suggesting new areas of study or potential therapeutic uses.

**5-6: Moderately Relevant**
   - The text mentions peptide research but might not delve into specifics about unnatural amino acids or detailed experimental validation.
   - The discussion on protein targets or computational models may be present but lacks depth.
   - The methodology is sound, but the impact on the field might be moderate or not immediately clear.
   - Potential applications or implications for peptide research are suggested but not thoroughly explored.

 **3-4: Somewhat Relevant**
   - The text briefly mentions aspects of peptide research but lacks specificity or detailed discussion.
   - Experimental validation, if mentioned, is vague or general.
   - There is minimal mention of protein targets or computational research, with little to no discussion on the implications or applications.
   - The relevance to current trends or issues in peptide research is minimal or tangential.

**1-2: Irrelevant**
   - The text has little to no mention of peptide research, unnatural amino acids, or experimental validation related to peptides.

        
        text to score:
        "{metadata}
        
        {summary}    
        
        {bullet_points}"
        
        remember to follow the scoring metric we are trying to assess how relevant the text was to peptide research and if it should be a priority for a peptide researcher to read it, if the majority of the discussion doesnt involve peptides its probably a low score
        
scoring metrics:

**9-10: Exceptionally Relevant**
- Advances peptide research with novel findings, including new peptides, mechanisms, or therapeutic applications.
- Demonstrates robust experimental validation and computational analysis targeting specific protein interactions, discusses many peptides and proteins, very high impact on the field of peptides.

**7-8: Highly Relevant**
- Directly contributes to peptide research with experimental evidence and computational insights, moderate to high impact on the field of peptides.
- Presents clear implications for the field, suggesting new research directions or therapeutic applications, mentions specific peptides and proteins

**5-6: Moderately Relevant**
- Discusses peptide research with some mention of methodology or protein targets but lacks depth
- Offers suggestions for the field with moderate impact or unclear applications, discusses atleast a few specific peptides and proteins or targets

**3-4: Somewhat Relevant**
- Briefly mentions peptide research without significant detail or depth, doesnt mention specific peptides or proteins by name, unclear impact on peptide research.
- Lacks clear experimental validation or computational analysis relevant to peptides.

**1-2: Irrelevant**
- Minimal or no mention of peptides, lacking relevance to the field of peptide research.



now give a score, always give a score, score only based on the metrics remeber the target audience is researchers who are used to jargon
        <end_of_turn>

        <start_of_turn>model-gemma
        """
        # Process the input with the tokenizer and model
        input_ids = tokenizer(input_text, return_tensors="pt").to("cuda")
        outputs = model.generate(**input_ids, max_new_tokens=8000)

        # Extract and return the model's output, removing the initial prompt from the response
        score_output = tokenizer.decode(outputs[0], skip_special_tokens=True)
        score_start = score_output.find("model-gemma\n") + len("model-gemma\n")
        score = score_output[score_start:].strip()

        # Append the extracted score to the scores list
        scores.append(score)
        # print(scores[0])

        extraction_input_text = f"""
<start_of_turn>user
give back the score that was given in the following text, just give back the score nothing else:




{scores[0]}

<end_of_turn>
<start_of_turn>model-gemma

"""
        input_ids = tokenizer(extraction_input_text, return_tensors="pt").to("cuda")
        extraction_outputs = model.generate(**input_ids, max_new_tokens=8000)
        extracted_score = tokenizer.decode(
            extraction_outputs[0], skip_special_tokens=True
        )
        extracted_start = extracted_score.find("model-gemma\n") + len("model-gemma\n")
        extracted_score = extracted_score[extracted_start:].strip()

        # Append the extracted score to the scores list and the extracted numerical score to score_values list

        score_values.append(extracted_score)
        # Find all numbers in the extracted score string and convert them to integers
        numbers = [int(num) for num in re.findall(r"\d+", extracted_score)]

        # Check if we have extracted any numbers, then find and append the lowest one
        if numbers:
            lowest_score = min(numbers)
            lowest_scores.append(lowest_score)
        else:
            # In case no numbers were found, append a placeholder or handle as needed
            lowest_scores.append(None)

        if lowest_scores[0] == None:
            lowest_scores[0] = 0

    # Depending on your needs, you can return both the detailed scores and the extracted numerical scores
    return scores[0], score_values[0], lowest_scores[0]
