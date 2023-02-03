### welcome_assignment_answers
### Input - All nine questions given in the assignment.
### Output - The right answer for the specific question.

def welcome_assignment_answers(question):
    #Students do not have to follow the skeleton for this assignment.
    #Another way to implement is using a "case" statements similar to C.
    q_and_a = {
        "In Slack, what is the secret passphrase posted in the #lab-python-getting-started channel posted by a TA?": "mTCP",
        "Are encoding and encryption the same? - Yes/No": "No",
        "Is it possible to decrypt a message without a key? - Yes/No": "No",
        "Is it possible to decode a message without a key? - Yes/No": "Yes",
        "Is a hashed message supposed to be un-hashed? - Yes/No": "No",
        "What is the SHA256 hashing value to the following message: 'NYU Computer Networking' - Use SHA256 hash generator and use the answer in your code": "883c13da6a24949c9a23231b60119e2ace58459da4f8bbdd812cc37764548bdd",
        "Is MD5 a secured hashing algorithm? - Yes/No": "No",
        "What layer of the TCP/IP model does the protocol DNS belong to? - The answer should be an integer number": 2,
        "What layer of the TCP/IP model does the protocol ICMP belong to? - The answer should be an integer number": 3
    }
    return(q_and_a[question])
# Complete all the questions.


if __name__ == "__main__":
    #use this space to debug and verify that the program works
    debug_question = "What layer of the TCP/IP model does the protocol DNS belong to? - The answer should be an integer number"
    print(welcome_assignment_answers(debug_question))

#Questions:
#"In Slack, what is the secret passphrase posted in the #lab-python-getting-started channel posted by a TA?":
#"Are encoding and encryption the same? - Yes/No":
#"Is it possible to decrypt a message without a key? - Yes/No":
#"Is it possible to decode a message without a key? - Yes/No":
#"Is a hashed message supposed to be un-hashed? - Yes/No":
#"What is the SHA256 hashing value to the following message: 'NYU Computer Networking' - Use SHA256 hash generator and use the answer in your code":
#"Is MD5 a secured hashing algorithm? - Yes/No":
#"What layer of the TCP/IP model does the protocol DNS belong to? - The answer should be an integer number":
#"What layer of the TCP/IP model does the protocol ICMP belong to? - The answer should be an integer number":