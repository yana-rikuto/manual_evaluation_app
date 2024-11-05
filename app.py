from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)

# 動画フォルダのパスを修正
VIDEO_FOLDER = os.path.join('static', 'videos')
videos = [f for f in os.listdir(VIDEO_FOLDER) if f.endswith('.mp4')]

# CSVファイルのパス
CSV_FILE = 'ratings.csv'

# 初回実行時にCSVファイルを作成
if not os.path.exists(CSV_FILE):
    pd.DataFrame(columns=["動画ファイル名", "滑らかさ得点", "リズム感得点", "表現力得点"]).to_csv(CSV_FILE, index=False)

@app.route('/')
def index():
    if not videos:
        return "動画がありません。"

    return render_template('index.html', video_file=videos[0])

@app.route('/rate', methods=['POST'])
def rate():
    if 'video_file' not in request.form:
        return redirect(url_for('index'))

    video_file = request.form['video_file']
    smoothness = request.form.get('smoothness', type=int)
    rhythm = request.form.get('rhythm', type=int)
    expression = request.form.get('expression', type=int)

    # 評価データをCSVに保存
    df = pd.DataFrame([[video_file, smoothness, rhythm, expression]],columns=["動画ファイル名", "滑らかさ得点", "リズム感得点", "表現力得点"])
    df.to_csv(CSV_FILE, mode='a', header=False, index=False)

    # 次の動画に移行
    next_video_index = videos.index(video_file) + 1
    if next_video_index < len(videos):
        next_video = videos[next_video_index]
    else:
        return "すべての動画が評価されました。ご協力いただきありがとうございます！"

    return render_template('index.html', video_file=next_video)

if __name__ == '__main__':
    app.run(debug=True)
