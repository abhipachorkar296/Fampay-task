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