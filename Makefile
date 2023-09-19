.DELETE_ON_ERROR:

ROM = samuraishodown.sfc
ASM = hack.asm
PYTHON = python3
SCRIPT = fix-button-menu.py
OPTIONS = options.sfc
HACK = hack.sfc
SYM = hack.sym
OBJS = $(HACK) $(OPTIONS) $(SYM)

AS = asar
ASFLAGS = --symbols=wla

$(HACK): $(ASM) $(OPTIONS)
	cp $(OPTIONS) $(HACK)
	$(AS) $(ASFLAGS) $(ASM) $(HACK)

$(OPTIONS): $(SCRIPT)
	$(PYTHON) $(SCRIPT)

.PHONY:
clean:
	rm -rf $(OBJS)
