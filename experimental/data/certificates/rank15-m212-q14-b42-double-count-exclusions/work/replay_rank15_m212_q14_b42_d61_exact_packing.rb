#!/usr/bin/env ruby
# frozen_string_literal: true

require "digest"

SOURCE_SHA = "f44b6d8a93ef5e44a50fd7bce35ce85fbd83667c636bf0f4784c46500e44784d"
path = File.join(__dir__, "explore_rank15_m212_q14_b42_d46_d59_exact_packing.rb")
raise "packing source drift" unless Digest::SHA256.file(path).hexdigest == SOURCE_SHA

source = File.binread(path)
needle = "(46..59).each do |double_count|"
replacement = "(61..61).each do |double_count|"
raise "packing range anchor drift" unless source.scan(needle).length == 1
eval(source.sub(needle, replacement), TOPLEVEL_BINDING, path)
