#!/bin/bash
schedule="1"
while getopts 's:' flag; do
  case "${flag}" in
    s) schedule="${OPTARG}" ;;
  esac
done
if [ ${schedule} = "0" ] ; then
  scrapy crawl spidi 2> logs.log
else
  python scheduler.py 2> logs.log
fi

