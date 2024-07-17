import os
import random
from openai import OpenAI, RateLimitError, OpenAIError
import time

class Generator:
    def __init__(self):
        # Initialize the OpenAI API client with the provided API key
        # api_key = "API-KEY" uncomment and insert the API key
        self.client = OpenAI(api_key = "sk-proj-XOX5vmHAo6y8FbiuWF6OT3BlbkFJfP6tysmkkijxt51XDHdR")

        print("prompting AI model...")
        # Define a generic prompt for content generation
        self.phishing_prompt = f"""
            Based on the following blog post content and related subreddit discussions, generate a thoughtful and engaging comment to be posted under a related topic. The comment should reflect the key points and themes from both the blog post and the subreddit discussions.

            Blog Post Content:
            [blog_content]

            Subreddit Discussions:
            [subreddit_content]

            Comment:
            """
            
    def generate_content(self, blog_content, subreddit_content):
        
        completion_text = None
        retries = 3
        
        for i in range(retries):
            try:
                # Replace the placeholders with the content
                placeholders = {
                    "[blog_content]": blog_content,
                    "[subreddit_content]": subreddit_content
                }
                print("prompting AI model...")
                prompt_with_placeholders = self.phishing_prompt
                for placeholder, value in placeholders.items():
                    prompt_with_placeholders = prompt_with_placeholders.replace(placeholder, value)

                # Define the prompt and completion parameters
                parameters = {
                    "messages": [
                        {
                            "role": "assistant",
                            "content": prompt_with_placeholders,
                        }
                    ],
                    "model": "gpt-3.5-turbo",
                }
                print("AI model generating comment...")
                response = self.client.chat.completions.create(**parameters)
                print("Content successfully generated...")
                # Extract the completion text from the response
                completion_text = response.choices[0].message.content.strip()
                
            except RateLimitError as e:
                print(f"Rate limit exceeded, retrying in {2 ** i} seconds...")
                time.sleep(2 ** i)
            except OpenAIError as e:
                print(f"An error occurred: {e}")
                break

        return completion_text


def main():
    # Initialize the Generator
    generator = Generator()

    blog_content = "\nHomeTips, stories, insights, investigations, and how-tos about cloud storage.Topics related to backing up data, including backup strategies and techniques, and technical details and insights about backup.Bootstrapping, start-up tales and challenges, marketing mayhem, and more.Topics related to Backblaze products and releases, as well as Backblaze new hires, job postings, things around the office, irreverent humor, and more.Articles that explore our technical content more deeply, and are often geared towards our developer audience.Your space to read up on our latest partnership announcements, partner content, and more.May 9, 2024 byPat Patterson // No CommentsOver the past few years, since long before the recent large language model (LLM) revolution, we’ve benefited not only from the ability of AI models to transcribe audio to text, but also to automatically tag video files according to their content. Media asset management (MAM) software—such as Backlight iconik and Axle.ai (both Backblaze Partners, by the way)—allows media professionals to quickly locate footage by searching for combinations of tags. For example, “red car”, will return not only a list of video files containing red cars, but also the timecodes pinpointing the appearance of the red car in each clip.San Francisco startup Twelve Labs has created a video understanding platform that allows any developer to build this kind of functionality, and more, into their app via a straightforward RESTful API.\xa0In preparation for our webinar with Twelve Labs last month, I created a web app to show how to integrate Twelve Labs with Backblaze B2 for storing video. The complete sample app is available as open source at GitHub; in this blog post, I’ll provide a brief description of the Twelve Labs platform, explain how presigned URLs allow temporary access to files in a private bucket, and then share the key elements of the sample app. If you just want a high level understanding of the integration, read on, and feel free to skip the technical details!The core of the Twelve Labs platform is a foundation model that operates across the visual, audio, and text modes of video content, allowing multimodal video understanding. When you submit a video using the Twelve Labs Task API, the platform generates a compact numerical representation of the video content, termed an embedding, that identifies entities, actions, patterns, movements, objects, scenes, other elements of the video, and their interrelationships. The embedding contains everything the Twelve Labs platform needs to do its work—after the initial scan, the platform no longer needs access to the original video content. As each video is scanned into the platform, its embedding is added to an index, so this scanning process is often referred to as indexing.As part of the indexing process, the platform extracts a standard set of data from each video: a thumbnail image, a transcript of any spoken content, any text that appears on screen, and a list of brand logos, all annotated with timecodes locating them on the video’s timeline, and all accessible via the Twelve Labs Index API.You can have the platform create a title and summary, and even prompt the model to describe the video, via Twelve Labs’ Generate API. For example, I indexed an eight-minute video that explains how to back up a Synology NAS to Backblaze B2, then prompted the Generate API, “What are the two Synology applications mentioned in the video?” This was the first sentence of the resulting text:The two Synology applications mentioned throughout the video are “Synology Hyper Backup” and “Synology Cloud Sync.”The remainder of the response is a brief summary of the two applications and how they differ; here’s the full text. Although it does have that “AI flavor” as you read it, it’s clear and accurate. I must admit, I was quite impressed!You can define a taxonomy for your videos via the Classify API. Submit a one- or two-level classification schema and a set of video IDs, and the platform will assign each video to a category.Rounding up this quick tour of the Twelve Labs platform, the Search API, as its name suggests, allows you to search the indexed videos. As well as a search query, you must specify a set of content sources: any combination of visual, conversation, text in video, or logos. Each search result includes timecodes for its start and end.Now you understand the basic capabilities of the Twelve Labs platform, let’s look at how you can integrate it with Backblaze B2.A key feature of the sample app is that it uploads videos to a private Backblaze B2 Bucket, where they are only accessible to authorized users. Twelve Labs’ API allows you to submit a video for indexing by POSTing a JSON payload including the video’s URL to its Task API. This is straightforward for video files in a public bucket, but how do we allow the Twelve Labs platform to read files from a private bucket?One way would be to create an application key with capabilities to read files from the private bucket and share it with the Twelve Labs platform. The main drawback to this approach is that the platform currently lacks the ability to sign requests for files from a private bucket.Since Twelve Labs only needs to read the video file when we submit it for indexing, we can send it a presigned URL for the video file. As well as the usual Backblaze B2 endpoint, bucket name, and object key (path and filename), a presigned URL includes query parameters containing data such as the time when the URL was created, its validity period in seconds, an application key ID (or access key ID, in S3 terminology), and a signature created with the corresponding application key (secret access key). Here’s an example, with line breaks added for clarity:This URL was created at 22:26:52 UTC on 04/23/2024, and was valid for one hour (3600 seconds). The signature is 64 hex characters. Changing any part of the URL, for example, the X-Amz-Date parameter, invalidates the signature, resulting in an HTTP 403 Forbidden error when you try to use it, with a corresponding message in the response payload:Attempting to use the presigned URL after it expires yields HTTP 401 Unauthorized with a message such as:You can create presigned URLs with any of the AWS SDKs or the AWS CLI. For example, with the CLI:Presigned URLs are useful whenever you want to provide temporary access to a file in a private bucket without having to share an application key for a client app to sign the request itself. The sample app also uses them when rendering HTML web pages. For example, all of the thumbnail images are retrieved by the user’s browser via presigned URLs.Note that presigned URLs are a feature of Backblaze B2’s S3 Compatible API. Creating a presigned URL is an offline operation and does not consume any API calls. We recommend you use presigned URLs rather than the b2_get_download_authorization B2 Native API operation, since the latter is a class C API call.The sample app is written in Python, using JavaScript for its front end, the Django web framework for its backend, the Huey task queue for managing long-running tasks, and the Twelve Labs Python SDK to interact with the Twelve Labs platform. A simple web UI allows the user to upload videos to the private bucket, browse uploaded videos, submit them for indexing, view the resulting transcription, logos, etc., and search the indexed videos.Most of the application code is concerned with rendering the web UI; very little code is required to interact with Twelve Labs.The Django settings.py file defines a constant for the Twelve Labs index ID and creates an SDK client object using the Twelve Labs API key. Note that the app reads the index ID and API key from environment variables, rather than including the values in the source code. Externalizing the index ID as an environment variable allows more flexibility in deployment while, of course, you should never include secrets such as passwords or API keys in source code!When the web application starts, it validates the index ID and API key by retrieving details of the index."
    subreddit_content = """ Class B & C Transactions has charges of  $0.004 per 1,000 after the first 2,500 calls


            But nowhere it mentions the command "sync", not in the free list, not in the paid list


            Anyone knows?

            Title: Bidirectional B2 Cloud Replication?
            Content: Hi,

            Is it allowed/safe to have two B2 cloud replication rules that are like:

            Rule #1:

            Source Bucket (US East):
            holder-data-demo

            Destination Bucket (US West):
            holder-data-demo-mirror

            Rule #2:

            Source Bucket (US West):
            holder-data-demo-mirror

            Destination Bucket (US East):
            holder-data-demo

            For context, I'm trying to allow our application (which uploads data) to failover to `holder-data-demo-mirror` whenever US East is down, and have the data automatically sync back to `holder-data-demo` whenever it's back up.

            Title: B2 Upload help!
            Content: Howdy y'all i am using the B2 storage with typescript and currently have a "working" function for uploading using the api. The help i need is because it is currently using 'do_not_verify' for checksum. For some reason when calculating sha1 for a file the value i calculate doesn't survive on upload and i get

                {
                code: 'bad_request',
                message: 'Checksum did not match data received',
                status: 400
                }

            which could mean that my sha1 is bad however when a file with no data just a name is sent it goes though with: 

                GOOD
                {
                accountId: -',
                action: 'upload',
                bucketId: '-',
                contentLength: 0,
                contentMd5: 'd41d8cd98f00b204e9800998ecf8427e',
                contentSha1: 'da39a3ee5e6b4b0d3255bfef95601890afd80709',
                contentType: 'text/plain',
                fileId: '4_zbf7fc02cc2d2dde28fe40114_f415d8b5d983b4dfa_d20240509_m033242_c004_v0402022_t0058_u01715225562387',
                fileInfo: {},
                fileName: 'Y3KPuxI1lK7BjiQNZrkcv.txt',
                fileRetention: {
                    isClientAuthorizedToRead: true,
                    value: { mode: null, retainUntilTimestamp: null }
                },
                legalHold: { isClientAuthorizedToRead: true, value: null },
                serverSideEncryption: { algorithm: null, mode: null },
                uploadTimestamp: 1715225562387
                }

            with the Sha1 always matching. so i was wondering if my files were getting corrupted in flight, also no, using do not verify it uploads fine.

            Anyone experience anything similar?

            https://pastebin.com/pYx6ybfg

            Title: B2 Pricing
            Content: Can anyone explain to me how $5/TB is breakeven cost for backblaze? From what I can tell breakeven is a lot closer to $1.50/TB on average.

            Title: Backblaze B2 no longer free for first 10GB?
            Content: I checked the pricing page and it seems to suggest a pay-as-you-go monthly fee is necessary. Previously there was mention that the first 10GB was free, but that has disappeared.

            Edit: seems like it's available in the tooltips, so I guess that clears it up. If anyone from Backblaze is reading this, probably can consider improving UX to make the info available outside of a tooltip (it's neither searchable nor readable unless I hovered).

            Title: Issue with Windows B2 Self-Contained CLI
            Content: Hi guys,


            I've been trying to adapt CORS rules to be allowed to access the B2 API from my browser. I am having trouble with the following official documentation: https://www.backblaze.com/docs/cloud-storage-enable-cors-with-the-cli.



            I copied the command written in the documentation near the end of the page for Windows B2 Self-Contained CLI:  
            `b2-windows.exe update-bucket --corsRules "[{\"corsRuleName\":\"downloadFromAnyOrigin\", \"allowedOrigins\": [\"https\"], \"allowedHeaders\": [\"range\"], \"allowedOperations\": [\"b2_download_file_by_id\", \"b2_download_file_by_name\"], \"exposeHeaders\": [\"x-bz-content-sha1\"], \"maxAgeSeconds\": 3600}]" bucketName allPublic`   

            Where I changed the "update-bucket" into "bucket update" as per new requirements. I also renamed "bucketName" into the name of my bucket. After writing the command, the error I get is:

            b2.exe bucket update: error: argument bucketType: invalid choice: 'corsRuleName\\\\:\\\\downloadFromAnyOrigin\\\\, \\\\allowedOrigins\\\\: \[\\\\https\\\\\], \\\\allowedHeaders\\\\: \[\\\\range\\\\\], \\\\allowedOperations\\\\: \[\\\\b2\_download\_file\_by\_id\\\\, \\\\b2\_download\_file\_by\_name\\\\\], \\\\exposeHeaders\\\\: \[\\\\x-bz-content-sha1\\\\\], \\\\maxAgeSeconds\\\\: 3600}\]' (choose from 'allPublic', 'allPrivate')


            I don't know how to resolve this issue now and I'm stuck. I would be extremely grateful if someone could help me out with this. Thank you!"""
                    
    comment = generator.generate_content(blog_content, subreddit_content)
    
    print(comment)
if __name__ == "__main__":
    main()


