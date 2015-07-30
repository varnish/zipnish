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
			}
		},

		watch: {
			options: {
				livereload: {
					host: '10.0.2.15',
					port: 35729
				}
			},

			configFiles: {
				files: ['Gruntfile.js'],
				options: {
					reload: true,
					spawn: false,
          livereload: false
				}
			},

			css: {
				files: ['scss/*.scss'],
				tasks: ['clean:bootstrap', 'sass:dev'],
				options: {
					spawn: false,
				}
			},

			templates: {
				files: ['../../ui/app/templates/*.html'],
				options: {
					spawn: false,
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
	grunt.loadNpmTasks('grunt-contrib-connect');

	// Default Task
	grunt.registerTask('default', ['connect']);
};
