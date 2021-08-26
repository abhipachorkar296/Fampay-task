from django.conf import settings
from django.shortcuts import render
from django.views.generic.base import View
from rest_framework import serializers
from rest_framework import status
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from task.models import Videos
from task.serializers import VideosSerializer
from task.pagination import MyPage, CustomPagination
from django.utils import timezone
from datetime import timedelta
from task.search import BM25
import nltk

API_KEY_LIST = settings.API_KEY
# Create your views here.
def save_videos(videos):
	for video in videos:
		id = video["id"]["videoId"]
		title = video["snippet"]["title"]
		description = video["snippet"]["description"]
		urls = video["snippet"]["thumbnails"]["default"]["url"]
		created_datetime = video["snippet"]["publishTime"]
		
		data = {
			"id" : id,
			"title" : title,
			"description" : description,
			"urls" : urls,
			"created_datetime" : created_datetime
		}
		serializer = VideosSerializer(data=data)
		if(serializer.is_valid()):
			serializer.save()
		else:
			break

def fetch_videos():
	url = "https://www.googleapis.com/youtube/v3/search"
	publishedAfter = (timezone.now() - timedelta(days=500)).strftime("%Y-%m-%dT%H:%M:%SZ")
	parameters = {
		"q" : "football",
		"part" : "snippet",
		"order" : "date",
		"type" : "video",
		"maxResult" : 50,
		"publishedAfter" : publishedAfter,
		"key" : API_KEY_LIST[0]
	}
	total_pages = 5
	for API_KEY in API_KEY_LIST:
		parameters["key"] = API_KEY
		response = requests.get(url,params=parameters)
		if(response.status_code == 200):
			page_number = 1
			response_data = response.json()
			videos = response_data["items"]
			next_page_token = response_data["nextPageToken"]
			save_videos(videos)
			while(page_number < total_pages and next_page_token):
				page_number += 1
				parameters["pageToken"] = next_page_token
				response = requests.get(url, params=parameters)
				if(response.status_code == 200):
					response_data = response.json()
					videos = response_data["items"]
					next_page_token = response_data["nextPageToken"]
					save_videos(videos)
				else:
					break

			break

class GetVideos(APIView, MyPage):
	pagination_class = CustomPagination
	def get(self, request):
		videos = Videos.objects.all()
		page = self.paginate_queryset(videos)

		if page is not None:
			serializers = VideosSerializer(page, many=True)
			return self.get_paginated_response(serializers.data)

		serializers = VideosSerializer(videos, many=True)
		return Response(data=serializers.data, status=status.HTTP_200_OK)

class SearchAlgo(APIView):
	def get(self,request, query):
		videos = Videos.objects.all()
		corpus = VideosSerializer(videos, many=True).data
		words = ["you'd", 'weren', 'his', 'they', 'too', 'those', "wasn't", "doesn't", 'shouldn', 'our', "weren't", 'yours', 'other', "haven't", 'above', 'y', 'not', 'my', 'myself', 'most', 'few', 'very', 'the', 'mustn', 'against', 'aren', 'until', 'these', 'below', 'how', 'because', "you've", 'her', 'ourselves', "couldn't", 'having', 'between', 'be', 'what', 'while', 'or', 'themselves', 'of', 'will', 'hasn', 'needn', 'only', "hasn't", 'have', 'before', 'no', 'any', 'isn', 'there', 'been', 'further', 'in', 'with', 'now', 'your', 'such', 'it', 'couldn', 're', "mustn't", 'did', 'this', 'hers', 'once', 'own', 'their', 'some', 'both', "aren't", 'again', 'down', 'has', 'where', 'had', 'are', 'don', 'ain', "you'll", 'after', 'she', "that'll", 'by', 'o', 'you', 'll', 'hadn', "don't", 'herself', 'yourself', "needn't", 't', 'didn', 'we', 'during', 'doing', "isn't", 'here', 'being', 'won', 'out', 'into', 'from', 'a', 've', 'i', 'its', 'himself', 'him', "wouldn't", "shan't", "she's", 'an', 'yourselves', 'haven', 'doesn', 'them', 'on', "it's", 'whom', 'as', 'should', 'when', 'who', 'to', 'me', 'wouldn', 'about', "won't", 'mightn', 'same', 'ma', "shouldn't", "you're", 'and', 'nor', 'up', 'that', 'were', 's', 'am', 'do', 'but', 'why', 'he', 'off', 'over', "mightn't", 'for', 'wasn', 'then', 'than', 'theirs', 'm', 'which', 'under', 'does', 'all', 'through', "didn't", 'at', 'shan', 'itself', 'so', 'is', "hadn't", 'was', 'd', 'just', 'each', 'can', "should've", 'ours', 'more', 'if']
		stopwords = set(words)
		texts = [
			[word for word in (document["title"]+document["description"]).lower().split() if word not in stopwords] for document in corpus
		]

		# build a word count dictionary so we can remove words that appear only once
		word_count_dict = {}
		for text in texts:
			for token in text:
				word_count = word_count_dict.get(token, 0) + 1
				word_count_dict[token] = word_count

		texts = [[token for token in text if word_count_dict[token] > 1] for text in texts]

		query = [word for word in query.lower().split() if word not in stopwords]

		bm25 = BM25()
		bm25.fit(texts)
		scores = bm25.search(query)
		results = []
		for score, doc in zip(scores, corpus):
			score = round(score, 3)
			results.append((score, doc))
		results.sort(key=lambda x:-x[0])
		data = [doc for _, doc in results[:10]]
		return Response(data=data, status=status.HTTP_200_OK)