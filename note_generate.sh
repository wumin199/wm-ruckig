#! /bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# exit when error
set -e

get_branch_name(){
  ## 如果git已经安装好了，则默认用当前分支名，否则用默认名称
  if git --version > /dev/null ; then
      branch_name=$(git rev-parse --abbrev-ref HEAD)
  else
      branch_name="notes.md"
  fi
  ## 防止有些起名是cmt/1st_20220610，不符合命名规则
  echo -e note_$(basename $branch_name).md
}


if [ $# -ne 1 ]; then
  echo -e "${YELLOW}usage: ./note_generate file_name${NC}"
  comment_file_name=$(get_branch_name)
  echo -e "${YELLOW}use [$comment_file_name] as default${NC}"
else
  # $1 会获取到 a，即 $1 对应传给脚本/函数的第一个参数
  comment_file_name=$1
fi




# 初始化
# $_ (下划线) 表示的是打印上一个输入参数行, 当这个命令在开头时, 打印输出文档的绝对路径名.
thisFile=$_ 

# 获取相对路径下的脚本名称
if [ $BASH ]  #/bin/bash
then
  thisFile=${BASH_SOURCE[0]}  # 脚本名称，相对路径
fi

# 获取脚本绝对路径
# > /dev/null 的目的是，将realpath $thisFile的输出，不显示处理, 否则会在终端打印出来
# >/dev/null 就是将标准输出和标准出错的信息屏蔽不显示
if realpath $thisFile > /dev/null ; then  # realpath 用于获取指定目录或文件的绝对路径。
  thisFile=$(realpath $thisFile)
else
  # $0 对应 "./test.sh" 这个值。如果执行的是 ./work/test.sh， 则对应 ./work/test.sh 这个值，而不是只返回文件名本身的部分。
  thisFile=$0   
fi

# 获取脚本所在文件夹路径
# cd过去再获取文件夹路径
projectDir=$(cd $(dirname $thisFile) && pwd)

make_sure_folder_does_not_exist() {
  # $1 会获取到 a，即 $1 对应传给脚本/函数的第一个参数
  if [[ -d $1 ]]; then
    error "Error: $1 does exist!"
    exit 1
  fi
}

# 创建文件夹并初始化
# $1 会获取到 a，即 $1 对应传给脚本/函数的第一个参数
create_file(){
    if [ -f $1 ]; then 
      rm -rf $1
    fi
    touch $1
    echo -e "update: $(date +'%Y-%m-%d %H:%M:%S')" > $1
    echo -e "------" >> $1
}

# 读取文件夹下的所有文件
# 通过echo来返回 -> 返回是字符串
# 递归函数要使用局部变量，不要使用全局变量
read_dir() {
  # 获取传入的目录/文件夹路径
  local dir=$1
  # 循环指定目录下的所有文件
  local files
  files=$(ls "$dir")
  for file in $files; do
    local path="$dir/$file" #指的是当前遍历文件的完整路径
    # 判断是否是目录，如果是目录则递归遍历，如果是文件则打印/返回该文件的完整路径
    if [ -d "$path" ]; then
      read_dir "$path"
    else
      echo -e "$path" # echo表示返回的意思
    fi
  done
}




generate_doc() {

  local note
  # 如果传递进来的参数<1
  if [ $# -ne 1 ]; then
    echo -e "${RED}Usage: generate_doc file${NC}"
    return
  fi

  # 文件的绝对路径
  file=$1

  # grep没有找到匹配的，由于set -e的存在，程序会直接退出来， 所以使用 { || }
  # -o 仅显示匹配到的字符串
  match_status=$({ grep -o "@[Ss][Tt][Aa][Tt][Uu][Ss].*$" $file || echo "" ; })
  match_summary=$({ grep -o "@[Ss][Uu][Mm][Mm][Aa][Rr][Yy].*$" $file || echo "" ; })
  match_study=$({ grep -o "@[Ss][Tt][Uu][Dd][Yy].*$" $file || echo "" ; })
  

  # 没匹配上，返回空
  # [] 两边要留出空格
  if [ -z "$match_study" ] && [ -z "$match_summary" ] && [ -z "$match_status" ]; 
  then
    # echo -e "exit"
    # echo -e "${RED}no match data${NC}"
    return
  fi

  # 获取文件相对路径，用来显示在markdown上，作为段落标题
  relative_file=${file#*$projectDir/}  # 截取字符串 http://c.biancheng.net/view/1120.html
  record_num=$(grep -i @study $1 | wc -l) # -i 忽略大小写



  note_title=$(echo "" | awk -v file=$relative_file '{print "\n##", file}')

  if [ -n "$match_status" ];
  then
    note_status=${match_status:1} # 从index=1开始截取字符串，去掉@
  else
    note_status="Status: None"
  fi

  if [ -n "$match_summary" ];
  then
    note_summary=${match_summary:1} # 截取字符串，去掉@
  else
    note_summary="Summary: None"
  fi

  # $ 表示正则表达式匹配到行尾
  # 注意指令中间不要留空格
  # awk -v 表示定义一个变量
  # awk $0: 输入匹配到的正行内容 ($1表示第一列内容，$2表示第2列内容... 默认是用空格来分割awk是输入内容)
  note_study=$(grep -o '@[Ss][Tt][Uu][Dd][Yy].*$' $file | \
  awk -v record_num=$record_num 'BEGIN{printf "\ncomments total: %d\n%s\n", record_num, "```yml"}{print $0}END{print "```"}')
  
  
  note=""
  note="$note_title\n\n$note_status\n\n$note_summary\n$note_study"
  echo -e "$note" # ""会原样输出，包含回车，换行

  # 其他方法2
  # grep -i @study $file | \
  # awk -v file=$relative_file -v record_num=$record_num 'BEGIN{printf "\n### %s\ntotal:%d\n%s\n", file, record_num, "---<<<"}{print $0}END{print "--->>>"}'

  # 其他方法3
  # awk -v file=$relative_file -v record_num=$record_num 'BEGIN{printf "\n### %s\ntotal:%d\n%s\n", file, record_num, "---<<<"} /@[Ss][Tt][Uu][Dd][Yy]/ {print $0} END{print "--->>>"}' $file



}

comment_file=$projectDir/$comment_file_name
create_file $comment_file


# 获取文件夹下的所有文件的完整绝对路径
ret_str=$(read_dir ${projectDir})
file_array=($ret_str)
# echo -e ${#file_array[*]} 

for i in ${!file_array[@]}
do
  if [ ${file_array[i]} != $thisFile ]; then
    if [ ${file_array[i]} != $comment_file ]; then
      # echo -e ${file_array[i]}
      note=$(generate_doc ${file_array[i]})
      # -n -> non zero
      if [ -n "$note" ]; then
        echo -e "$note" >> $comment_file
      fi
    fi
  fi
done

echo -e "${YELLO}generating...${NC}"
echo -e "${NC}generate $comment_file done ${NC}"