
from flask import Flask, render_template, request,send_file
from flask_cors import cross_origin
import datacollection
from pytube import YouTube


app = Flask(__name__)

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homepage():
    return render_template('homepage.html')


@app.route('/extract',methods=['POST', 'GET'])  # route to display the videos page
@cross_origin()
def videos_section():
    if request.method == 'POST':
        url=request.form['url']
        count= int(request.form['video_count'])
        fetched_data=datacollection.fetch_data(url,count)

        return render_template('videos.html',fetched_data= fetched_data, range=range, count=count)

@app.route('/video_comments/<videoid>',methods=['GET'])  # route to display the comments of the videos
@cross_origin()
def video_comments(videoid):
    extracted_comments=datacollection.fetch_singlevideo_comments(videoid)

    return render_template('comments.html',extracted_comments= extracted_comments)

@app.route('/download/<videoid>',methods=['GET'])  # route to download video
@cross_origin()
def download(videoid):
    yt=YouTube.from_id(videoid)
    ab=yt.streams[1].download()
    return send_file(ab, as_attachment=True, download_name='video.mp4', mimetype='video/mp4')


if __name__ == "__main__":
    app.run(debug=True)

