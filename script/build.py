
import os
import subprocess
import platform
import argparse
import multiprocessing

cpu_count = multiprocessing.cpu_count()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--build", help="build", type=str, default="")
    parser.add_argument("--clear", help="clear build", action="store_true")
    parser.add_argument("--install", help="install", action="store_true")
    args = parser.parse_args()

    if args.build == "Release" or args.build == "Debug":
        if platform.system() == "Linux":
            compile_command = "cmake -B build -S . " \
                              "-DBUILD_PYTHON_MODULE=ON" \
                              "-DCMAKE_TOOLCHAIN_FILE=/opt/vcpkg/scripts/buildsystems/vcpkg.cmake " \
                              "-DVCPKG_TARGET_TRIPLET=x64-linux -DCMAKE_PREFIX_PATH={}/wumin199 " \
                              "-DCMAKE_INSTALL_PREFIX={}/wumin199 " \
                              "-DCMAKE_BUILD_TYPE={} -G Ninja".format(args.build, args.build,
                                                                      args.build)
            os.system(compile_command)
            compile_command = "cmake --build build --config {} --parallel {}".format(args.build,
                                                                                     cpu_count - 2)
            os.system(compile_command)
        elif platform.system() == "Windows":
            compile_command = "cmake -B build -S . " \
                              "-DBUILD_PYTHON_MODULE=ON" \
                              "-DCMAKE_TOOLCHAIN_FILE=C:/vcpkg/scripts/buildsystems/vcpkg.cmake " \
                              "-DVCPKG_TARGET_TRIPLET=x64-windows -DCMAKE_PREFIX_PATH={}/wumin199 " \
                              "-DCMAKE_INSTALL_PREFIX={}/wumin199 " \
                              "-DCMAKE_BUILD_TYPE={} -G Ninja".format(args.build, args.build,
                                                                      args.build)
            windows_build_command = "powershell.exe Set-ExecutionPolicy Bypass -Scope Process -Force; c:/buildtools/vcvars-powershell.ps1;"
            subprocess.call("{};{}".format(windows_build_command, compile_command))
            compile_command = "cmake --build build --config {} --parallel {}".format(args.build,
                                                                                     cpu_count - 2)
            subprocess.call("{};{}".format(windows_build_command, compile_command))
        else:
            print("cannot decide CMAKE_TOOLCHAIN_FILE. unknown system {}".format(platform.system()))
    if args.clear:
        if platform.system() == "Linux":
            os.system("rm -rf build")
        elif platform.system() == "Windows":
            subprocess.call("powershell.exe Remove-Item ./build -Recurse -Force")
        else:
            print("cannot clear build directory. unknown system {}".format(platform.system()))
    if args.install:
        os.system("cmake --install build")
