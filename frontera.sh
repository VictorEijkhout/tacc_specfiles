#!/bin/bash

mkdir -p frontera_specfiles
for s in *.spec ; do
    cat $s \
	> frontera_specfiles/$s
done

cat install.sh \
    | sed -e 's/COMPILERS/i191,j19_9 i231,j21_9 g91,j19_9 g132,j21_9/' \
    | sed -e 's/#frontera:/s/#frontera: //' \
    > frontera_specfiles/install.sh

cd frontera_specfiles
chmod +x install.sh
# cat << EOF > README
# These files are generated by the "frontera.sh" script
# one level lower.
# EOF
