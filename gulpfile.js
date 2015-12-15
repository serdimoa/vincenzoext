/**
 * Created by serdimoa on 02.11.15.
 */
'use strict';

var gulp = require('gulp'),
    watch = require('gulp-watch'),
    prefixer = require('gulp-autoprefixer'),
    uglify = require('gulp-uglify'),
    sass = require('gulp-sass'),
    sourcemaps = require('gulp-sourcemaps'),
    cssmin = require('gulp-minify-css'),
    imagemin = require('gulp-imagemin'),
    pngquant = require('imagemin-pngquant'),
    rigger = require('gulp-rigger'),
    rimraf = require('rimraf');


var path = {
    build: { //Тут мы укажем куда складывать готовые после сборки файлы
        js: 'app/static/',
        js_admin: 'app/static/',
        css: 'app/static/',
        css_admin: 'app/static/',
        img: 'app/static/img/',
        plugins:'app/static/plugins',
        fonts:'app/static/fonts'
    },
    src: { //Пути откуда брать исходники
        js: 'js/main.js',//В стилях и скриптах нам понадобятся только main файлы
        js_admin: 'js/admin.js',//В стилях и скриптах нам понадобятся только main файлы
        style: 'css/admin.scss',
        style_admin: 'css/main.scss',
        img: 'img/**/*.*',//Синтаксис img/**/*.* означает - взять все файлы всех расширений из папки и из вложенных каталогов
        plugins: 'plugins/**/*.*',
        fonts:'fonts/**/*.*'
    },
    watch: { //Тут мы укажем, за изменением каких файлов мы хотим наблюдать
        js: 'js/main.js',
        js_admin: 'js/admin.js',
        style: 'css/main.scss',
        style_admin: 'css/admin.scss',
        img: 'img/**/*.*',
        fonts:'fonts/**/*.*'
    },
    clean: './build'
};

gulp.task('js:build', function () {
    gulp.src(path.src.js) //Найдем наш main файл
        .pipe(rigger()) //Прогоним через rigger
        .pipe(sourcemaps.init()) //Инициализируем sourcemap
        .pipe(uglify()) //Сожмем наш js
        .pipe(sourcemaps.write()) //Пропишем карты
        .pipe(gulp.dest(path.build.js));//Выплюнем готовый файл в build
});

gulp.task('js_admin:build', function () {
    gulp.src(path.src.js_admin) //Найдем наш main файл
        .pipe(rigger()) //Прогоним через rigger
        .pipe(sourcemaps.init()) //Инициализируем sourcemap
        .pipe(uglify()) //Сожмем наш js
        .pipe(sourcemaps.write()) //Пропишем карты
        .pipe(gulp.dest(path.build.js_admin));//Выплюнем готовый файл в build
});

gulp.task('style:build', function () {
    gulp.src(path.src.style) //Выберем наш main.scss
        .pipe(sourcemaps.init()) //То же самое что и с js
        .pipe(sass()) //Скомпилируем
        .pipe(prefixer()) //Добавим вендорные префиксы
        .pipe(cssmin()) //Сожмем
        .pipe(sourcemaps.write())
        .pipe(gulp.dest(path.build.css)); //И в build
});

gulp.task('style_admin:build', function () {
    gulp.src(path.src.style_admin) //Выберем наш main.scss
        .pipe(sourcemaps.init()) //То же самое что и с js
        .pipe(sass()) //Скомпилируем
        .pipe(prefixer()) //Добавим вендорные префиксы
        .pipe(cssmin()) //Сожмем
        .pipe(sourcemaps.write())
        .pipe(gulp.dest(path.build.css_admin)); //И в build
});

gulp.task('plugins:build',function(){
        gulp.src(path.src.plugins) //Выберем наши plugins
        .pipe(gulp.dest(path.build.plugins));//Выплюнем готовый файл в build
});

gulp.task('fonts:build',function(){
        gulp.src(path.src.fonts) //Выберем наши plugins
        .pipe(gulp.dest(path.build.fonts));//Выплюнем готовый файл в build
});

gulp.task('image:build', function () {
    gulp.src(path.src.img) //Выберем наши картинки
        .pipe(imagemin({ //Сожмем их
            progressive: true,
            svgoPlugins: [{removeViewBox: false}],
            use: [pngquant()],
            interlaced: true
        }))
        .pipe(gulp.dest(path.build.img)); //И бросим в build
});

gulp.task('build', [
    'js:build',
    'js_admin:build',
    'style:build',
    'style_admin:build',
    'image:build',
    'plugins:build',
    'fonts:build'
]);

gulp.task('watch', function(){

    watch([path.watch.style], function(event, cb) {
        gulp.start('style:build');
    });
    watch([path.watch.style_admin], function(event, cb) {
        gulp.start('style_admin:build');
    });
    watch([path.watch.js], function(event, cb) {
        gulp.start('js:build');
    });

    watch([path.watch.js_admin], function(event, cb) {
        gulp.start('js_admin:build');
    });

    watch([path.watch.img], function(event, cb) {
       gulp.start('image:build');
    });
    watch([path.watch.fonts], function(event, cb) {
        gulp.start('fonts:build');
    });


});

gulp.task('clean', function (cb) {
    rimraf(path.clean, cb);
});

gulp.task('default', ['build', 'watch']);
