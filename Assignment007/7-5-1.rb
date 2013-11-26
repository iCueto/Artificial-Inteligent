#!/usr/bin/env ruby

f = Array.new(5) { Array.new(6) {0.0} }
map = [
       [false] * 6,
       [false] + [true]*4 + [false],
       [false, true, false, true, true, false],
       [false] + [true]*4 + [false],
       [false] * 6,
      ]


def up(f, map)
  g = Array.new(5) { Array.new(6) {0.0} }

  1.upto(3) do |i|
    1.upto(4) do |j|
      if map[i+1][j]
        g[i+1][j] += f[i][j] * 0.8
      else
        g[i][j] += f[i][j] * 0.8
      end

      if map[i][j-1]
        g[i][j-1] += f[i][j] * 0.1
      else
        g[i][j] += f[i][j] * 0.1
      end

      if map[i][j+1]
        g[i][j+1] += f[i][j] * 0.1
      else
        g[i][j] += f[i][j] * 0.1
      end
    end

  end

  g
end

def right(f, map)
  g = Array.new(5) { Array.new(6) {0.0} }

  1.upto(3) do |i|
    1.upto(4) do |j|
      if map[i][j+1]
        g[i][j+1] += f[i][j] * 0.8
      else
        g[i][j] += f[i][j] * 0.8
      end

      if map[i+1][j]
        g[i+1][j] += f[i][j] * 0.1
      else
        g[i][j] += f[i][j] * 0.1
      end

      if map[i-1][j]
        g[i-1][j] += f[i][j] * 0.1
      else
        g[i][j] += f[i][j] * 0.1
      end
    end
  end

  g
end




f[1][1] = 1.0
f = up(f, map)
4.downto(0) { |i| p f[i] }
puts
f = up(f, map)
f = right(f, map)
f = right(f, map)
f = right(f, map)

4.downto(0) { |i| p f[i] }
