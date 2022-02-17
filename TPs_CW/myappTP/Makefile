# @Author: ronan
# @Date:   09-08-2016
# @Email:  ronan.lashermes@inria.fr
# @Last modified by:   ronan
# @Last modified time: 18-12-2020
# @License: GPL



#IDIR is dir with includes
#ODIR is output dir with .o
#SDIR is dir with sources (.c, .s)
# CDIR =$(shell pwd)
CDIR=.
IDIR =$(CDIR)
ODIR =$(CDIR)/obj
SDIR =$(CDIR)

TC=avr-

# Specify the compiler to use
CC=$(TC)gcc
# Specity the linker to use
LD=$(TC)gcc

OBJDUMP = $(TC)objdump
OBJCOPY = $(TC)objcopy

HAL=./hal
XMEGA_HAL=$(HAL)/xmega

#Targeting Xmega 128d4 (similar to d3)
TARGET = -mmcu=atxmega128d3
SS_VER =SS_VER_1_1
PLATFORM=CW303

#Compilation flags
CFLAGS += -I$(HAL)
CFLAGS += -I$(XMEGA_HAL)
CFLAGS += -I$(IDIR)
CFLAGS += $(TARGET)
CFLAGS += -fpack-struct
#Debug symbols
#CFLAGS += -g
#Optimizations
CFLAGS += -Os
CDEFS += -DSS_VER=$(SS_VER) -DPLATFORM=$(PLATFORM)

#Say where to look for some kinds of files
vpath %.c $(SDIR):$(XMEGA_HAL):$(HAL)
vpath %.h $(IDIR):$(XMEGA_HAL):$(HAL)

#Linker flags
LFLAGS = $(TARGET) -O1

#Dependencies
_DEPS = hal.h simpleserial.h aes.h avr_compiler.h xmega_hal.h uart.h usart_driver.h
DEPS = $(patsubst %,$(IDIR)/%,$(_DEPS))

#Object files to link
_OBJ = main.o aes.o simpleserial.o uart.o usart_driver.o xmega_hal.o
OBJ = $(patsubst %,$(ODIR)/%,$(_OBJ))


#C compilation rule
$(ODIR)/%.o: %.c $(DEPS)
	@echo CC $<
	@$(CC) -c -o $@ $< $(CFLAGS) $(CDEFS)

aes.hex: aes.elf $(DEPS)
	@echo "Generating hex file"
	@$(OBJCOPY) -O ihex $< $@

#Linking
aes.elf: $(ODIR) $(OBJ)
	@echo Linking...
	@$(LD) $(OBJ) $(LFLAGS) -o $@
	@$(OBJDUMP) -S $@ > $@.list
	@echo OK


$(ODIR):
	mkdir $@

#Cleaning
.PHONY: clean
clean:
	rm -f $(ODIR)/*.o *~ core $(INCDIR)/*~
	rm aes.elf aes.elf.list

