let SessionLoad = 1
let s:so_save = &g:so | let s:siso_save = &g:siso | setg so=0 siso=0 | setl so=-1 siso=-1
let v:this_session=expand("<sfile>:p")
silent only
silent tabonly
cd ~/self-clone
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
let s:shortmess_save = &shortmess
if &shortmess =~ 'A'
  set shortmess=aoOA
else
  set shortmess=aoO
endif
badd +1 t1.py
badd +1 term://~/self-clone//846:/bin/bash
badd +1 receiver_v2.py
badd +1 term://~/self-clone//862:/bin/bash
badd +1 term://~/self-clone//859:/bin/bash
badd +2 term://~/self-clone//871:/bin/bash
badd +3 char_to_freq.py
badd +1 t2.py
badd +1 term://~/self-clone//842:/bin/bash
argglobal
%argdel
$argadd t1.py
tabnew +setlocal\ bufhidden=wipe
tabrewind
edit t1.py
let s:save_splitbelow = &splitbelow
let s:save_splitright = &splitright
set splitbelow splitright
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd _ | wincmd |
split
1wincmd k
wincmd w
wincmd w
wincmd _ | wincmd |
split
1wincmd k
wincmd w
let &splitbelow = s:save_splitbelow
let &splitright = s:save_splitright
wincmd t
let s:save_winminheight = &winminheight
let s:save_winminwidth = &winminwidth
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
exe '1resize ' . ((&lines * 32 + 33) / 67)
exe 'vert 1resize ' . ((&columns * 120 + 120) / 240)
exe '2resize ' . ((&lines * 32 + 33) / 67)
exe 'vert 2resize ' . ((&columns * 120 + 120) / 240)
exe '3resize ' . ((&lines * 32 + 33) / 67)
exe 'vert 3resize ' . ((&columns * 119 + 120) / 240)
exe '4resize ' . ((&lines * 32 + 33) / 67)
exe 'vert 4resize ' . ((&columns * 119 + 120) / 240)
argglobal
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let &fdl = &fdl
let s:l = 7 - ((6 * winheight(0) + 16) / 32)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 7
normal! 010|
wincmd w
argglobal
if bufexists(fnamemodify("t2.py", ":p")) | buffer t2.py | else | edit t2.py | endif
if &buftype ==# 'terminal'
  silent file t2.py
endif
balt t1.py
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let &fdl = &fdl
let s:l = 1 - ((0 * winheight(0) + 16) / 32)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 1
normal! 0
wincmd w
argglobal
if bufexists(fnamemodify("receiver_v2.py", ":p")) | buffer receiver_v2.py | else | edit receiver_v2.py | endif
if &buftype ==# 'terminal'
  silent file receiver_v2.py
endif
balt t1.py
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let &fdl = &fdl
let s:l = 1 - ((0 * winheight(0) + 16) / 32)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 1
normal! 023|
wincmd w
argglobal
if bufexists(fnamemodify("term://~/self-clone//846:/bin/bash", ":p")) | buffer term://~/self-clone//846:/bin/bash | else | edit term://~/self-clone//846:/bin/bash | endif
if &buftype ==# 'terminal'
  silent file term://~/self-clone//846:/bin/bash
endif
balt t1.py
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 274 - ((31 * winheight(0) + 16) / 32)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 274
normal! 0
wincmd w
4wincmd w
exe '1resize ' . ((&lines * 32 + 33) / 67)
exe 'vert 1resize ' . ((&columns * 120 + 120) / 240)
exe '2resize ' . ((&lines * 32 + 33) / 67)
exe 'vert 2resize ' . ((&columns * 120 + 120) / 240)
exe '3resize ' . ((&lines * 32 + 33) / 67)
exe 'vert 3resize ' . ((&columns * 119 + 120) / 240)
exe '4resize ' . ((&lines * 32 + 33) / 67)
exe 'vert 4resize ' . ((&columns * 119 + 120) / 240)
tabnext
let s:save_splitbelow = &splitbelow
let s:save_splitright = &splitright
set splitbelow splitright
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd _ | wincmd |
split
1wincmd k
wincmd w
wincmd w
let &splitbelow = s:save_splitbelow
let &splitright = s:save_splitright
wincmd t
let s:save_winminheight = &winminheight
let s:save_winminwidth = &winminwidth
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
exe '1resize ' . ((&lines * 32 + 33) / 67)
exe 'vert 1resize ' . ((&columns * 120 + 120) / 240)
exe '2resize ' . ((&lines * 32 + 33) / 67)
exe 'vert 2resize ' . ((&columns * 120 + 120) / 240)
exe 'vert 3resize ' . ((&columns * 119 + 120) / 240)
argglobal
if bufexists(fnamemodify("term://~/self-clone//842:/bin/bash", ":p")) | buffer term://~/self-clone//842:/bin/bash | else | edit term://~/self-clone//842:/bin/bash | endif
if &buftype ==# 'terminal'
  silent file term://~/self-clone//842:/bin/bash
endif
balt char_to_freq.py
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 4 - ((3 * winheight(0) + 16) / 32)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 4
normal! 029|
wincmd w
argglobal
if bufexists(fnamemodify("term://~/self-clone//862:/bin/bash", ":p")) | buffer term://~/self-clone//862:/bin/bash | else | edit term://~/self-clone//862:/bin/bash | endif
if &buftype ==# 'terminal'
  silent file term://~/self-clone//862:/bin/bash
endif
balt term://~/self-clone//846:/bin/bash
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 4 - ((3 * winheight(0) + 16) / 32)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 4
normal! 029|
wincmd w
argglobal
if bufexists(fnamemodify("term://~/self-clone//859:/bin/bash", ":p")) | buffer term://~/self-clone//859:/bin/bash | else | edit term://~/self-clone//859:/bin/bash | endif
if &buftype ==# 'terminal'
  silent file term://~/self-clone//859:/bin/bash
endif
balt term://~/self-clone//862:/bin/bash
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 2 - ((1 * winheight(0) + 32) / 65)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 2
normal! 0
wincmd w
exe '1resize ' . ((&lines * 32 + 33) / 67)
exe 'vert 1resize ' . ((&columns * 120 + 120) / 240)
exe '2resize ' . ((&lines * 32 + 33) / 67)
exe 'vert 2resize ' . ((&columns * 120 + 120) / 240)
exe 'vert 3resize ' . ((&columns * 119 + 120) / 240)
tabnext 1
if exists('s:wipebuf') && len(win_findbuf(s:wipebuf)) == 0 && getbufvar(s:wipebuf, '&buftype') isnot# 'terminal'
  silent exe 'bwipe ' . s:wipebuf
endif
unlet! s:wipebuf
set winheight=1 winwidth=20
let &shortmess = s:shortmess_save
let &winminheight = s:save_winminheight
let &winminwidth = s:save_winminwidth
let s:sx = expand("<sfile>:p:r")."x.vim"
if filereadable(s:sx)
  exe "source " . fnameescape(s:sx)
endif
let &g:so = s:so_save | let &g:siso = s:siso_save
set hlsearch
nohlsearch
doautoall SessionLoadPost
unlet SessionLoad
" vim: set ft=vim :
