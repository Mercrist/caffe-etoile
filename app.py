from flask import Flask, url_for, redirect, request, render_template
import pymongo

app = Flask(__name__) #initialize flask app
