var gulp = require('gulp');
var del = require('del');
var mainBowerFiles = require('main-bower-files');
var debug = require('gulp-debug');
var gulpFilter = require('gulp-filter');
var concat = require('gulp-concat');
var less = require('gulp-less');
var coffee = require('gulp-coffee');
var flatten = require('gulp-flatten');
var order = require('gulp-order');
var livereload = require('gulp-livereload');
var templateCache = require('gulp-angular-templatecache');
var uglify = require('gulp-uglify');
var rename = require('gulp-rename');
var minifyCss = require('gulp-minify-css');
var sourcemaps = require('gulp-sourcemaps');


gulp.task('clean', function (cb) {
    return del(['./dist/*'], cb);
});

gulp.task('fontawesome-fonts', function () {
    return gulp.src('./bower_components/font-awesome/fonts/**')
        .pipe(gulp.dest('./dist/fonts'));
});

gulp.task('bootstrap-fonts', function () {
    return gulp.src('./bower_components/bootstrap/fonts/**')
        .pipe(gulp.dest('./dist/fonts'));
});

gulp.task('bower', ['bootstrap-fonts', 'fontawesome-fonts'], function () {
    var jsFilter = gulpFilter(['**/*.js'], {restore: true});
    var lessFilter = gulpFilter(['**/*.less'], {restore: true});
    var cssFilter = gulpFilter(['**/*.css'], {restore: true});
    return gulp.src(mainBowerFiles(), {base: 'bower_components'})
        .pipe(sourcemaps.init())
        .pipe(jsFilter)
        .pipe(concat('bower.js'))
        .pipe(uglify())
        .pipe(rename({
            suffix: ".min"
        }))
        .pipe(sourcemaps.write('./maps'))
        .pipe(gulp.dest('./dist'))
        .pipe(jsFilter.restore)
        .pipe(lessFilter)
        .pipe(less())
        .pipe(lessFilter.restore)
        .pipe(cssFilter)
        .pipe(concat('bower.css'))
        .pipe(minifyCss())
        .pipe(rename({
            suffix: ".min"
        }))
        .pipe(sourcemaps.write('./maps'))
        .pipe(gulp.dest('./dist'));
});

gulp.task('partials', function () {
    return gulp.src('./src/**/*.partial.html')
        .pipe(flatten())
        .pipe(templateCache({module: 'app'}))
        .pipe(gulp.dest('./dist'));
});

gulp.task('scripts', function () {
    return gulp.src('./src/**/*.coffee')
        .pipe(sourcemaps.init())
        .pipe(coffee({bare: true}))
        .pipe(order([
            "**/*.module.js"
        ]))
        .pipe(concat('src.js'))
        .pipe(sourcemaps.write('./maps'))
        .pipe(gulp.dest('./dist'));
});

gulp.task('styles', function () {
    return gulp.src('./src/**/*.css')
        .pipe(sourcemaps.init())
        .pipe(concat('styles.css'))
        .pipe(minifyCss())
        .pipe(rename({
            suffix: ".min"
        }))
        .pipe(sourcemaps.write('./maps'))
        .pipe(gulp.dest('./dist'));
})

gulp.task('assets', function () {
    return gulp.src('./src/app/assets/**')
        .pipe(gulp.dest('./dist/assets'));
});

gulp.task('index', function () {
    return gulp.src('./src/index.html')
        .pipe(gulp.dest('./dist'));
});

gulp.task('watch', function () {
    gulp.watch('./bower_components/**', ['bower']);
    gulp.watch('./src/**/*.partial.html', ['partials']);
    gulp.watch('./src/**/*.coffee', ['scripts']);
    gulp.watch('./src/**/*.css', ['styles']);
    gulp.watch('./src/app/assets/**', ['assets']);
    gulp.watch('./src/index.html', ['index']);
    livereload.listen();
    gulp.watch('./dist/**').on('change', livereload.changed);
})

gulp.task('default', ['clean'], function () {
    gulp.start('partials', 'scripts', 'assets', 'bower', 'index', 'styles');
});