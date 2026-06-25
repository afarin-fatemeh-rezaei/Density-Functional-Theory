#!/bin/bash

pseudos=("Al.pbesol-n-kjpaw_psl.1.0.0.UPF" "Al.rel-pbe-nl-rrkjus_psl.1.0.0.UPF")
k_grids=("4 4 4 0 0 0" "6 6 6 0 0 0" "8 8 8 0 0 0" "10 10 10 0 0 0")
ecut="60"

for pseudo in "${pseudos[@]}"; do
  folder="Al-$(echo "$pseudo" | cut -d. -f2)"
  mkdir -p "$folder"

  if [[ $pseudo == *"rel-pbe"* ]]; then
    noncolin=".true."
    lspinorb=".true."
  else
    noncolin=".false."
    lspinorb=".false."
  fi

  for k in "${k_grids[@]}"; do
    k_num=$(echo "$k" | awk '{print $1}')
    k_str="${k_num}${k_num}${k_num}"
    input_file="$folder/Al.scf.$ecut.$k_str.in"
    output_file="$folder/Al.scf.$ecut.$k_str.out"

    sed "s|<PSEUDO_DIR>|../pseudo|g;
         s|<PSEUDO>|$pseudo|g;
         s|<KPOINTS>|$k|g;
         s|<NONCOLIN>|$noncolin|g;
         s|<LSPINORB>|$lspinorb|g" input_template.in > "$input_file"

    (cd "$folder" && pw.x -in "Al.scf.$ecut.$k_str.in" > "Al.scf.$ecut.$k_str.out")
  done
done
