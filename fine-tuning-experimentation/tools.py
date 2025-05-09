import pandas as pd
from torch import device, cuda, Tensor
from sentence_transformers import SentenceTransformer, util

device = device('cuda' if cuda.is_available() else 'cpu')


class tools():

    def encode_description(model: SentenceTransformer, description: str):
        try:
            return model.encode(description)
        except:
            return None
    
    def generate_encodings(df: pd.DataFrame, model_name: str):

        # import the selected model from the sentence-transformers framework
        model = SentenceTransformer(model_name)
        model.to(device)

        df[model_name] = df['description'].map(lambda x: tools.encode_description(model, x))

        # return the dataframe with the embeddings
        return df
    
    



    def rr_k(prompt: pd.Series, df: pd.DataFrame, model_name: str, duplicate_ids: set, k: int):
    
        similarity_scores = [] # array that will store tuples with a report id and its similarity score with the prompt

        # iterate trough the dataframe
        for index, row in df.iterrows():
            
        
            # append current report id and cosine similarity for the current report
            # and the prompt descriptions the the selected model has generated
            try:
                similarity_scores.append(
                    (
                        index, 
                        util.cos_sim(
                            prompt[model_name],
                            row[model_name]
                        )
                    )
                )
            except:
                pass
                
        
        # sort the similarity_scores list based on the similarity scores in descending order
        similarity_scores.sort(key=lambda x: -x[1])

        relevant_at_top_k = 0 # initialize counter of identified duplicates in top k as 0

        # iterate trough the tuples in the similarity_scores array. We skip the first since it will be the prompt itself
        for value in similarity_scores[1:k+1]:

            # if the current report is a duplicate of the prompt, increase relevant_at_top_k by one
            if value[0] in duplicate_ids:
                relevant_at_top_k += 1

        # the recall rate at k is the number of duplicates retrieved in the first k over the total number of duplicates
        recall_rate = relevant_at_top_k / len(duplicate_ids)
        return recall_rate
    

    def rr_k_dict(prompt: Tensor, tensor_dict: dict, model_name: str, duplicate_ids: set, k: int):
    
        similarity_scores = [] # array that will store tuples with a report id and its similarity score with the prompt

        # iterate trough the dataframe
        for bug_id in tensor_dict:
            
        
            # append current report id and cosine similarity for the current report
            # and the prompt descriptions the the selected model has generated
            try:
                similarity_scores.append(
                    (
                        bug_id, 
                        util.cos_sim(
                            prompt,
                            tensor_dict[bug_id]
                        )
                    )
                )
            except:
                pass
                
        
        # sort the similarity_scores list based on the similarity scores in descending order
        similarity_scores.sort(key=lambda x: -x[1])

        relevant_at_top_k = 0 # initialize counter of identified duplicates in top k as 0

        # iterate trough the tuples in the similarity_scores array. We skip the first since it will be the prompt itself
        for value in similarity_scores[1:k+1]:

            # if the current report is a duplicate of the prompt, increase relevant_at_top_k by one
            if value[0] in duplicate_ids:
                relevant_at_top_k += 1

        # the recall rate at k is the number of duplicates retrieved in the first k over the total number of duplicates
        recall_rate = relevant_at_top_k / len(duplicate_ids)
        return recall_rate
