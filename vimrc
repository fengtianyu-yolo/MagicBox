set nocompatible              " be iMproved, required
filetype off                  " required

set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()

Plugin 'VundleVim/Vundle.vim'
Plugin 'davidhalter/jedi-vim' " 代码提示
Plugin 'Lokaltog/vim-powerline' " 状态栏
Plugin 'Yggdroot/indentLine' " 缩进对齐
Plugin 'vim-syntastic/syntastic' " 语法检查
Plugin 'scrooloose/nerdtree' " 文件目录
Plugin 'vim-scripts/indentpython.vim' " python缩进
Plugin 'kien/ctrlp.vim' " ctrl+p 文件搜索
Plugin 'vim-scripts/taglist.vim'

call vundle#end()            " required
filetype plugin indent on    " required

" plugin config
let g:indentLine_char='|'
let g:indentLine_enabled=1

let g:syntastic_check_on_open = 1 " 启动打开语法检查
set statusline+=%#warningmsg#

let NERDTreeChDirMode=1
let NERDTreeShowBookmarks=1
let NERDTreeWinSize=25

let Tlist_WinWidth=24
let Tlist_Ctags_Cmd='/usr/local/Cellar/ctags/5.8_1/bin/ctags'
let Tlist_File_Fold_Auto_Close=1
let Tlist_Exit_OnlyWindow=1 "窗口只有taglist时自动关闭
let Tlist_Use_Right_Window=1 " 在窗口右侧打开
let Tlist_Auto_open=1 " 自动打开
let Tlist_Show_One_File=1 " 只显示当前文件的tag

let mapleader = "-"

" key binding
map <F5> :call CompileRun()<CR>
map <F2> :NERDTreeToggle<CR>
map <F3> :TlistToggle<CR>
map <C-J> <C-W><C-J>
map <C-H> <C-W><C-H>
map <C-K> <C-W><C-K>
map <C-L> <C-W><C-L>
map <leader>c yaw
map <leader>v vaw"0p

" 自动命令
autocmd BufNewFile *.py exec ":call InsertFirstLine()"

" custom func
" 编译运行代码
func! CompileRun()
	exec "w"
	if &filetype == 'python'
		exec "!time python3 %"
	endif
endfunc

" python自动插入第一行文件
function InsertFirstLine()
	if &filetype == 'python'
		call setline(1, '#! /usr/bin/local/python3')
	endif
endfunction

" custom config
colorscheme desert
set nu
syntax on
set foldmethod=indent
set foldlevel=99
set tabstop=4
set shiftwidth=4
set softtabstop=4
set hlsearch
