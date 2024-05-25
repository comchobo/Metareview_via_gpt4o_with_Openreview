# Metareview OpenReview papers using gpt-4o

I tried reviewing paper using gpt-4o, however it was not that easy to read pdf formatted papers. So, I just crawled Openreview comments and tried gpt-4o to review the paper. Surprisingly, it could manage to review those, in almost the same depth as me.

The code is embarrassingly simple.

`pip install -r requirements.txt`

`python main.py --OpenReview_id 'your_openreview_id' --OpenReview_pwd 'your_openreview_pwd' --venue_name 'ICLR.cc/2024/Conference' --openai_api_key 'your_openai_api_key' --session_type 'oral'`

will just return the requests. This will review oral papers in ICLR 2024.

It takes 20 seconds to review reviews(?) and $0.05 was spent.
