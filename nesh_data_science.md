## Nesh Data Science Interview
### Author: Viginesh Vaibhav Muraliraman


### 1. Graph Database Question:  How would you extract all the information related to Project node (Entity)?

There are three categories of information to be extracted from the given Project node:

1. **Information about Project node (primary information):** These can be accessed directly by querying to retrieve all of the attributes of that node.
2. **Information directly related to Project node (secondary information):** These can be accessed by querying for all the nodes that have a direct relationship with Project node (i.e., nodes in the graph DB (Database) with edges pointing to the given Project node).
3. **Information indirectly related to Project node (tertiary information):** These can be accessed by querying for all the nodes that share at least one common attribute value with the given Project node, for select attributes. Such nodes may not have any direct links to the Project node itself, but may provide contextual information for the given node. For example, let's assume that the Project nodes have an attribute to record the names of its stakeholders. Then, 2 Project nodes may share the same set (or subset) of stakeholders, which can be found by querying for nodes with the same values for the 'stakeholder' attribute. Care should be taken to do this only on a **select subset of attributes**, because not all of the attributes in the Project node will have relevant contextual information. For example, attributes like the start date and end date of a project aren't important here because 2 projects with the same start/end dates are only related coincidentally. 

 In this manner, we could query and obtain all the relevant information associated with the Project node, and rank the results by the category of the information extracted. Here, the primary and secondary information are the most relevant because they are directly related to the Project node, while the tertiary information could be used to augment/refine the results for any future queries made on the node.

### 2. Text Document Question: How would you develop an optimized search engine that can retrieve the top most relevant documents of the provided query?

The first step would be to categorize the information found in the text documents. A lot of recent research in Natural Language Processing has focused on entity extraction [1], which we could leverage to solve this problem. For example, Yangfeng Ji et al. [2] proposed a system called **EntitiyNLM** to identify entities in sentences, and dynamically build/update the relationship between the identified entities. For example, consider the following sentence: "_John wanted to visit a coffee shop in downtown Copenhagen. He was told that it has the best beans!_" [2].  When this sentence is processed by the EntityNLM model,  here's what happens:

- ‘John’, ‘the coffee shop’ and ‘downtown Copenhagen’ are identified as entities
- Pronoun 'he' is co-referenced to 'John'
- Pronoun 'it' is co-referenced to 'the coffee shop'
- 'Best beans' is inferred as a feature related to 'the coffee shop'

Using such a model, we could implement the following:

1. Declare the kinds of entities to be recognized from the document (projects, people, etc.).
2. Identify all entities of interest from the text documents, and categorize them by the types declared in the previous step.
3. Extract the relationship between the given entities.
4. Use the extracted information to build a graph database, where each node is the an entity and the relationship between entities is represented as edges,
5. Some of the extracted entities may also be encoded as attributes for the nodes in the graph DB. This can be done by explicitly declaring which types of the extracted entities are attributes.

Once we have built the graph database, we then apply the above entity extraction model on the user's query to understand the entities described in the query itself (e.g., identifying the project name, location, start date, etc. in the query). Then, we implement the steps described in my previous answer to extract all the relevant information from the graph DB for all the entities and/or their attributes mentioned in the given query. We can then rank the query results based on the categories of the information extracted (primary, secondary and tertiary), and display the results with the highest rank. Care should be taken to rank the extracted primary and secondary information higher than any tertiary information.

### References

1. [Gatt, Albert, and Emiel Krahmer. "Survey of the state of the art in natural language generation: core tasks, applications and evaluation."](https://pdfs.semanticscholar.org/d13b/b317e87f3f6da10da11059ebf4350b754814.pdf) _Journal of Artificial Intelligence Research_ 61.1 (2018): 65-170.
2. [Ji, Yangfeng, et al. "Dynamic Entity Representations in Neural Language Models."](https://www.aclweb.org/anthology/D17-1195.pdf) _Proceedings of the 2017 Conference on Empirical Methods in Natural Language Processing_. 2017.
 

