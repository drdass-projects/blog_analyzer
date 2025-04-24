#!/bin/bash
KEYWORD="test"
FILENAME="report"
curl "http://localhost:8000/fetch-and-analyze?keyword=${KEYWORD}&filename=${FILENAME}"
