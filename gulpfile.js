var basePaths = {
    src: 'frontdev/',
    dest: 'src/static/'
};

var paths = {
    fonts: {
        src: basePaths.src + 'font/',
        dest: basePaths.dest + 'font/'
    },
    images: {
        src: basePaths.src + 'img/',
        dest: basePaths.dest + 'img/'
    },
    scripts: {
        src: basePaths.src + 'js/',
        dest: basePaths.dest + 'js/'
    },
    styles: {
        src: basePaths.src + 'sass/',
        dest: basePaths.dest + 'css/'
    },
};

var appFiles = {
    fonts: paths.fonts.src + '**',
    images: paths.images.src + '**',
    scripts: paths.scripts.src + '**',
    scriptsBrowserify: paths.scripts.src + '*.js',
    styles: paths.styles.src + '**/*.scss',
};

/*Let the magic begin*/

var gulp = require('gulp'),
    del = require('del'),
    compass = require('gulp-compass'),
    path = require('path'),
    gutil = require('gulp-util'),
    minifyCSS = require('gulp-minify-css'),
    livereload = require('gulp-livereload'),
    browserify = require('gulp-browserify'),
    gulpif = require('gulp-if'),
    uglify = require('gulp-uglify');
    imagemin = require('gulp-imagemin');

    isProduction = false;


gulp.task('clean', function(cb) {
    del([basePaths.dest, basePaths.src + 'css'], cb);
});

gulp.task('copy', function() {
    gulp.src(paths.fonts.src + '**')
        .pipe(gulp.dest(paths.fonts.dest));
    gulp.src(paths.images.src + '**')
        .pipe( gulpif ( isProduction, imagemin ({
            progressive: true,
            svgoPlugins: [{removeViewBox: false}]
        }) ) )
        .pipe(gulp.dest(paths.images.dest))
        .pipe(livereload());
});

gulp.task('compass', function() {
    gulp.src(appFiles.styles)
        .pipe(compass({
            sass: paths.styles.src,
            css: basePaths.src + 'css',
            font: paths.fonts.src,
            image: paths.images.src
        }))
        .pipe(gulpif(isProduction, minifyCSS()))
        .pipe(gulp.dest(paths.styles.dest))
        .pipe(livereload());
});

gulp.task('scripts', function() {
  gulp.src(appFiles.scriptsBrowserify)
      .pipe(browserify({
        insertGlobals: false,
        debug: false
      }))
      .pipe(gulpif(isProduction, uglify()))
      .pipe(gulp.dest(paths.scripts.dest));
});

// Rerun the task when a file changes
gulp.task('watch', function() {
    livereload.listen();
    gulp.watch(appFiles.images, ['copy']);
    gulp.watch(appFiles.fonts, ['copy']);
    gulp.watch(appFiles.styles, ['compass']);
    gulp.watch(appFiles.scripts, ['scripts']);
});

gulp.task('default', ['clean'], function() {
    // gulp.start('compass', 'copy', 'scripts', 'watch');
    gulp.start('compass', 'copy', 'watch');
});

gulp.task('dist', ['clean'], function() {
    isProduction = true;
    gulp.start('compass', 'copy', 'scripts');
});
