source $2/config/shell_config.ini
projectDir=$1
outputs=$3
echo "Project directory: $projectDir, out puts: $outputs"
cd $projectDir
if [ "$TEST" = false ]; then
	ls
	# ./gradlew assembleBrazilDebug --stacktrace
	./gradlew assembleGlobalDebug --stacktrace

	if [ ! -d "${outputs}" ]; then
		rm -rf ${outputs}
		mkdir ${outputs}
	else
		mkdir ${outputs}
	fi
	# cp -rf ${projectDir}/app/build/outputs/apk/brazil/debug ${outputs}
	cp -rf ${projectDir}/app/build/outputs/apk/global/debug ${outputs}
	echo "fetch your apk in $outputs"
fi
