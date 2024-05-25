import json, os
from tqdm import tqdm
from LLM_paper_reviewer import LLM_Reviewer
from paper_crawler import OpenReviewCrawler
from utils import make_path


def main(args):
    make_path(args.input_path)
    make_path(args.output_path)

    crawler = OpenReviewCrawler(username=args.OpenReview_id, password=args.OpenReview_pwd,
                                venue_name=args.venue_name)
    llm_reviewer = LLM_Reviewer(openai_api_key=args.openai_api_key)

    crawler.download_reviews(review_paper_path=args.input_path, session_type=args.session_type)

    papers = [x[:-5] for x in os.listdir(args.input_path)]
    for paper_file in tqdm(papers):
        with open(f'{args.input_path}/{paper_file}.json', 'r') as f:
            review_text = json.load(f)
        res_indirect = llm_reviewer.review_indirectly(pdf_text=review_text['qna'])
        review_text['reviews'] = res_indirect
        with open(f'{args.output_path}/{paper_file}.json', 'w') as f:
            json.dump(review_text, f, indent=4)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_path', default='cache')
    parser.add_argument('--output_path', default='Indirectly_reviewed_papers')
    parser.add_argument('--session_type', default='oral')
    parser.add_argument('--OpenReview_id',default='')
    parser.add_argument('--OpenReview_pwd', default='')
    parser.add_argument('--venue_name', default='')
    parser.add_argument('--openai_api_key', default='')
    args = parser.parse_args()

    main(args)
