var gulp = require('gulp');
var inject = require('gulp-inject');
var concat = require('gulp-concat');
var print = require('gulp-print');
var angularFilesort = require('gulp-angular-filesort');
var uglify = require('gulp-uglify');
var ts = require("gulp-typescript");

gulp.task('css-task', function () {
    var customCssStream = gulp.src([
        './bower_components/bootstrap/dist/css/bootstrap.min.css',
        './bower_components/bootstrap/dist/css/bootstrap-theme.min.css',
        './bower_components/fontawesome/css/font-awesome.min.css',
        './src/app.css'
    ]);

    return gulp.src('../server/static/index.html')
        .pipe(inject(
            customCssStream
                .pipe(print())
                .pipe(concat('confckurator.css'))
                .pipe(gulp.dest('../server/static/css/')),
            {name: 'styles', relative: true}
        ))
        .pipe(gulp.dest('../server/static/'));
});

gulp.task('compile-ts', ['css-task'], function () {
    var tsProject = ts.createProject("src/tsconfig.json");
    return tsProject.src()
        .pipe(tsProject())
        .js.pipe(gulp.dest(".build/ts/"));
});

gulp.task('js-task', ['compile-ts'], function () {
    var vendorStream = gulp.src([
        './bower_components/bootstrap/dist/js/bootstrap.min.js',
        './bower_components/jquery/dist/jquery.min.js',
        './bower_components/angular-bootstrap/ui-bootstrap-tpls.min.js',
        './bower_components/angular/angular.min.js',
        '.build/ts/api/**/*.js'
    ]);
    var appStream = gulp.src([
        '.build/ts/confckurator.js',
        '.build/ts/templates.js',
        '.build/ts/packs.js'
    ]);

    return gulp.src('../server/static/index.html')
        .pipe(inject(
            vendorStream
                .pipe(print())
                .pipe(angularFilesort())
                .pipe(concat('vendor.js'))
                .pipe(gulp.dest('../server/static/js/')),
            {name: 'vendor', relative: true}
        ))
        .pipe(inject(
            appStream
                .pipe(print())
                .pipe(concat('confckurator.js'))
                .pipe(uglify())
                .pipe(gulp.dest('../server/static/js/')),
            {name: 'app', relative: true}
        ))
        .pipe(gulp.dest('../server/static/'));
});

gulp.task('copy-fonts', ['js-task'], function(){
    return gulp.src([
        './bower_components/fontawesome/fonts/*',
        './bower_components/bootstrap/dist/fonts/*'
    ])
        .pipe(gulp.dest('../server/static/fonts'));
});

gulp.task('default', ['copy-fonts'], function () {
});
