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
% gunzip -c B.B00 > vmkBoot.ELF32-psigned
% gunzip -c WEASELIN.T00 > weaselin-weasel.vtar
```

Проверяем, что мы получили

```
% file vmkBoot.ELF32-psigned
B.B00.uncompressed: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), statically linked, not stripped

% file weaselin-weasel.vtar
WEASELIN.T00.uncompressed: tar archive
```

## Модифицируем B.B00

ТУТ ВСТАВИТЬ СКРИНШОТЫ ПО РЕДАКТИРОВАНИЮ

После редактирования собираем файл обратно

```
% mv B.B00 B.B00.backup
% gzip vmkBoot.ELF32-psigned
% mv vmkBoot.ELF32-psigned.gz B.B00
```

Проверяем, что мы получили тоже самое

```
% file B.B00
B.B00: gzip compressed data, was "vmkBoot.ELF32-psigned", last modified: Fri Jun  7 08:24:34 2024, from Unix, original size modulo 2^32 2110092
```

## Модифицируем WEASELIN.T00

ТУТ ВСТАВИТЬ СКРИНШОТЫ ПО РЕДАКТИРОВАНИЮ

123

Так же я написал скрипт на python3 (vtar.py) для работы с vtar архивами.

Распаковка:

```
python3.11 vtar.py -C weaselin_extracted -x weaselin-weasel.vtar
```

Далее открываем файл "weaselin_extracted/usr/lib/vmware/weasel/util/upgrade_precheck.py".

Ищем строку "`family == 0x06 and model`" и меняем "`0x36`" на "`0x01`".

Запаковка:

```
% mv WEASELIN.T00 WEASELIN.T00.backup
% mv weaselin-weasel.vtar weaselin-weasel.vtar.backup

% python3.11 vtar.py -c -C weaselin_extracted weaselin-weasel.vtar
% gzip weaselin-weasel.vtar
% mv weaselin-weasel.vtar.gz WEASELIN.T00
```

Проверяем, что получили тоже самое:

```
% file WEASELIN.T00
WEASELIN.T00: gzip compressed data, was "weaselin-weasel.vtar", last modified: Fri Jun  7 08:28:15 2024, from Unix, original size modulo 2^32 2506752
```

ДОПОЛНИТЬ
