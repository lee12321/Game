from apps import blueprint
from flask import render_template, request, url_for, send_from_directory, abort
from flask_ckeditor import upload_success, upload_fail
import os
from apps.models.BlogModel import Blog, Featured
from apps.models import db
from sqlalchemy import extract
from datetime import date, datetime, timedelta


PAGE_SIZE = 3


def get_archives(all_posts):
    dateSet = set()
    for blog in all_posts:
        if len(dateSet) >= 10: break
        dateSet.add(blog.date.strftime("%Y-%m"))
    return list(dateSet)


@blueprint.route('/', methods=['GET'])
def index():
    archive_flag = False
    older = False
    if request.args.get('date', ''):
        # 如果有日期参数，通过日期查询归档
        date_string = request.args.get('date', '')
        query_date = date_string.split('-')
        # 查询出所有请求日期下的文章
        recent = Blog.query.filter(Blog.is_delete == 0).filter(extract('year', Blog.date) == query_date[0]).filter(
            extract('month', Blog.date) == query_date[1])
        # 归档查询标记
        archive_flag = date_string
        # 归档查询只有一页
        page = 0
    else:
        # 查询最近的文章
        if request.args.get('page', ''):
            try:
                page = int(request.args.get('page', ''))
            except:
                page = 1
        else:
            page = 1
        # 更据页码参数查出
        recent = Blog.query.filter(Blog.is_delete == 0).order_by(Blog.date.desc()).offset(
            (page - 1) * PAGE_SIZE).limit((page - 1) * PAGE_SIZE + PAGE_SIZE).all()
        # 查询是否存在下一页
        next_page = Blog.query.filter(Blog.is_delete == 0).order_by(Blog.date.desc()).offset(
            page * PAGE_SIZE).limit(page * PAGE_SIZE + PAGE_SIZE).all()
        older = True if len(next_page) > PAGE_SIZE else False

    all_posts = Blog.query.filter(Blog.is_delete == 0).order_by(Blog.date.desc()).all()
    date_set = get_archives(all_posts)
    featured = Featured.query.filter(Blog.is_delete == 0).first()
    print(featured)
    return render_template('front/index.html',
                           blogs=recent,
                           dateSet=date_set,
                           page=page,
                           older=older,
                           featured=featured,
                           archive_flag=archive_flag)


@blueprint.route('/detail', methods=['GET'])
def detail():
    try:
        blog = Blog.query.filter(Blog.is_delete == 0).filter_by(id=request.args.get('id', 0)).first()
    except:
        return abort(404)

    if not blog: return abort(404)
    return render_template('front/detail.html', blog=blog)



# @blueprint.route('/files/<path:filename>')
# def uploaded_files(filename):
#     # ckeditor get images
#     path = os.path.abspath('./static/images')
#     return send_from_directory(path, filename)

# @blueprint.route('/upload', methods=['POST'])
# def upload():
#     # ckeditor upload
#     f = request.files.get('upload')
#     # Add more validations here
#     extension = f.filename.split('.')[1].lower()
#     if extension not in ['jpg', 'gif', 'png', 'jpeg']:
#         return upload_fail(message='Image only!')
#     f.save(os.path.join(os.path.abspath('./static/images'), f.filename))
#     url = url_for('blueprint.uploaded_files', filename=f.filename)
#     return upload_success(url=url)  # return upload_success call
