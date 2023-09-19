!JOYPAD_TMP         = $08
!ACTIONS_TMP        = $0c
!MASK_HARD_SLASH    = $c54f
!MASK_HARD_KICK     = $c551
!ACTION_H_SLASH     = $0030
!ACTION_H_KICK      = $00c0

hirom

org $df33bd
        ; don't combine masks for HARD(1) and HARD(2) buttons
        nop
        nop
        nop

org $c049f0
        ; don't add HARD modifier to L-SLASH
        nop
        nop

org $c04a00
        ; don't add HARD modifier to M-SLASH
        nop
        nop

org $c04a10
        ; don't add HARD modifier to L-KICK
        nop
        nop

org $c04a20
        ; don't add HARD modifier to M-KICK
        nop
        nop

org $c04a24
        jmp     my_code

org $c0ff40
my_code:
.check_for_hard_slash_press
        lda     !JOYPAD_TMP
        and     !MASK_HARD_SLASH, y
        beq     .check_for_hard_kick_press
        lda     #!ACTION_H_SLASH
        ora     !ACTIONS_TMP
        sta     !ACTIONS_TMP
.check_for_hard_kick_press
        lda     !JOYPAD_TMP
        and     !MASK_HARD_KICK, y
        beq     .end
        lda     #!ACTION_H_KICK
        ora     !ACTIONS_TMP
        sta     !ACTIONS_TMP
.end
        ; replace original instruction
        lda     !ACTIONS_TMP
        rts
