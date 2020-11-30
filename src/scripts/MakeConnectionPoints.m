clear
clc
close all
%% Setup

width = 80;
height = 40;

point_spacing = 10; % 10 pixels per grid unit

points_per_vertical_side = height/point_spacing + 1;
points_per_horizontal_side = width/point_spacing + 1;


%% Making the vectors

N = 2*(points_per_horizontal_side + points_per_vertical_side);

coordinates = zeros(N, 2);

p = 0;

for i = 0:1
    for j = 0:1/(points_per_vertical_side-1):1
        p = p + 1;
        coordinates(p,:) = [i,j];
    end
end

for i = 0:1
    for j = 0:1/(points_per_horizontal_side-1):1
        p = p + 1;
        coordinates(p,:) = [j,i];
    end
end

% output_string = zeros(10, N+2);
output_string = "points=[";

for i=1:N
%     temp_string = append(['[', string(coordinates(i,1)), ',', string(coordinates(i,2)), '],' ]);
    temp_string = "[" + string(coordinates(i,1)) + "," + string(coordinates(i,2)) + "],";
    output_string = output_string + temp_string;
end
output_string = char(output_string);
output_string = output_string(1:end-1);
output_string = string(output_string) + "];";
disp(output_string)
% figure
% plot(coordinates(:,1), coordinates(:,2), '*')