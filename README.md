# Модификация ESXi

## Подготовка

Копируем файлы B.B00 и WEASELIN.T00 в отдельную директорию.

Проверим заголовки файлов:

```
% file B.B00
B.B00: gzip compressed data, was "vmkBoot.ELF32-psigned", last modified: Tue Oct 26 00:50:37 2021, from Unix, original size modulo 2^32 2110091

% file WEASELIN.T00
WEASELIN.T00: gzip compressed data, was "weaselin-weasel.vtar", last modified: Tue Oct 26 01:19:06 2021, from Unix, original size modulo 2^32 4730880
```

Установим расширение "**Hex Editor**" в VSCode для редиктирования HEX.

Установим gunzip:

```
brew install gzip
```

Распаковка архивов:

```
% gunzip -c B.B00 > B.B00.uncompressed
% gunzip -c WEASELIN.T00 > WEASELIN.T00.uncompressed
```

Проверяем, что мы получили

```
% file B.B00.uncompressed
B.B00.uncompressed: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), statically linked, not stripped

% file WEASELIN.T00.uncompressed
WEASELIN.T00.uncompressed: tar archive
```

## Модифицируем B.B00

ТУТ ВСТАВИТЬ СКРИНШОТЫ ПО РЕДАКТИРОВАНИЮ

После редактирования собираем файл обратно

```
% gzip B.B00.uncompressed
% mv B.B00.uncompressed.gz B.B00
```

## Модифицируем WEASELIN.T00

ТУТ ВСТАВИТЬ СКРИНШОТЫ ПО РЕДАКТИРОВАНИЮ

123

Распаковываем WEASELIN.T00.uncompressed:

```
% mkdir weaselin_extracted
% tar -xvf WEASELIN.T00.uncompressed -C weaselin_extracted
```

123

Так же я написал скрипт на python3 (vtar.py) для работы с vtar архивами.

Распаковка:

python3.11 vtar.py -C test -x WEASELIN.T00.uncompressed

123
