module.exports = function (grunt) {

	grunt.initConfig({
		pkg: grunt.file.readJSON('package.json'),

		clean: {
			bootstrap: ['ui/app/static/css/bootstrap.css']
		},

		sass: {
			dev: {
				options: {
					compass: true,
					sourcemap: 'none',
					style: 'expanded'
				},
				files: {
					'../../ui/app/static/css/bootstrap.css': 'scss/bootstrap.scss'
				}
			},

			dist: {
				options: {
					compass: true,
					sourcemap: 'none',
					style: 'compressed'
				},
				files: {
					'../../ui/app/static/css/bootstrap.css': 'scss/bootstrap.scss'
				}
			},

			watch: {
				configFiles: {
					files: ['Gruntfile.js'],
					options: {
						reload: true
					}
				},

				css: {
					files: 'scss/*.scss',
					tasks: ['clean:bootstrap', 'sass:dev'],
					options: {
						livereload: true
					}
				}
			}
		}
	});

	// Distribution
	grunt.registerTask('dist', ['sass:dist']);

	// Development
	grunt.registerTask('dev', ['clean:bootstrap', 'sass:dev']);

	// Load NPM Tasks
	grunt.loadNpmTasks('grunt-contrib-clean');
	grunt.loadNpmTasks('grunt-contrib-sass');
	grunt.loadNpmTasks('grunt-contrib-watch');

	// Default Task
	grunt.registerTask('default', ['watch:css']);
};