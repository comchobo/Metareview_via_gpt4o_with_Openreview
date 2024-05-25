import openreview, os, json
from utils import make_path
from tqdm import tqdm


class OpenReviewCrawler:
    def __init__(self, username='', password='', venue_name = ''):
        self.openreview_client = openreview.api.OpenReviewClient(
            baseurl='https://api2.openreview.net',
            username=username,
            password=password
        )
        self.venue_name=venue_name

    def download_reviews(self, review_paper_path='', session_type='oral'):
        make_path(review_paper_path)
        submissions_temp = self.openreview_client.get_all_notes(content={'venueid': self.venue_name},
                                                                details='replies')
        oral_submissions = [submissions_temp[x] for x in range(len(submissions_temp))
                            if session_type in submissions_temp[x].content['venue']['value']]

        for oral_submission in tqdm(oral_submissions):
            user_id_dict = {x['id']: x['signatures'][0].split('/')[-1] for x in oral_submission.details['replies']}
            user_id_dict[oral_submission.details['replies'][0]['forum']] = 'Authors'
            user_ids = [[user_id_dict[x['id']], user_id_dict[x['replyto']]] for x in oral_submission.details['replies']]

            qna_texts = ''
            for user_id, qna in zip(user_ids, oral_submission.details['replies']):
                if user_id[0] == user_id[1]:
                    qna_texts += f'\n``` Authors to Reviewers\n'
                else:
                    qna_texts += f'\n``` {user_id[0]} to {user_id[1]}\n'
                qna = qna['content']
                if qna.get('summary', False):
                    qna_texts += '\nSummary: ' + qna['summary']['value']
                    qna_texts += '\nStrengths: ' + qna['strengths']['value']
                    qna_texts += '\nWeaknesses: ' + qna['weaknesses']['value']
                    qna_texts += '\nQuestions: ' + qna['questions']['value']
                elif qna.get('comment', False):
                    qna_texts += '\nReply: ' + qna['comment']['value']
                else:
                    qna_texts += '\nMetaReview: ' + qna['metareview']['value']
                    break
                qna_texts += '\nConversation finished ```\n'

            filename = oral_submission.details['replies'][0]['signatures'][0].split('/')[-2]
            qna_output = {'title' : oral_submission.content['title']['value'], 'qna' : qna_texts}
            with open(f'{review_paper_path}/{filename}.json', 'w') as f:
                json.dump(qna_output, f)
