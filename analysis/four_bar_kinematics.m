% =====================================================================
% four_bar_kinematics.m
% Kinematic analysis of the Clawbit four-bar linkage (ball sorter).
%
% Solves the linkage over one crank revolution with Freudenstein's
% equation, classifies the mechanism (Grashof), and reports the rocker
% swing angle, transmission angle range, and coupler curve extents.
%
% Units: millimetres and degrees. Runs in MATLAB or GNU Octave.
% =====================================================================

clear; clc; close all;

%% ------------------------------------------------------------------
% Link lengths -- REPLACE with measurements from your SolidWorks model.
%   r1: ground (frame pivot to pivot)
%   r2: crank (input, motor-driven)
%   r3: coupler
%   r4: rocker (output, drives the sorting gate)
% ------------------------------------------------------------------
r1 = 120;
r2 = 35;
r3 = 110;
r4 = 90;

%% ------------------------------------------------------------------
% Grashof classification
% ------------------------------------------------------------------
lens = sort([r1, r2, r3, r4]);
s = lens(1); l = lens(4); p = lens(2); q = lens(3);
link_names = {'ground (r1)', 'crank (r2)', 'coupler (r3)', 'rocker (r4)'};
[~, shortest_idx] = min([r1, r2, r3, r4]);

fprintf('--- Grashof analysis ---\n');
if s + l < p + q
    fprintf('s + l = %.1f < p + q = %.1f  -> Grashof chain\n', s + l, p + q);
    switch shortest_idx
        case 1
            kind = 'double-crank (shortest link is ground)';
        case 2
            kind = 'crank-rocker (shortest link is the crank)';
        case 3
            kind = 'double-rocker (shortest link is the coupler)';
        case 4
            kind = 'crank-rocker (shortest link is the rocker)';
    end
elseif s + l == p + q
    kind = 'change-point (folds flat under load: avoid for a sorter)';
else
    kind = 'NON-GRASHOF: no link can fully rotate - recheck link lengths!';
end
fprintf('Shortest link: %s\n', link_names{shortest_idx});
fprintf('Type: %s\n\n', kind);

%% ------------------------------------------------------------------
% Position analysis (Freudenstein's equation)
%   k1*cos(phi) - k2*cos(psi) + k3 = cos(phi - psi)
% solved for the rocker angle psi at each crank angle phi.
% ------------------------------------------------------------------
k1 = r1 / r2;
k2 = r1 / r4;
k3 = (r2^2 - r3^2 + r4^2 + r1^2) / (2 * r2 * r4);

N = 361;
phi = linspace(0, 360, N);
psi = zeros(1, N);      % rocker angle, open assembly branch
cx  = zeros(1, N);      % coupler midpoint trace (coupler curve)
cy  = zeros(1, N);
mu  = zeros(1, N);      % transmission angle

O2 = [0, 0];
O4 = [r1, 0];

for i = 1:N
    A = cosd(phi(i)) + k2;
    B = sind(phi(i));
    C = k1 * cosd(phi(i)) + k3;
    disc = A^2 + B^2 - C^2;
    if disc < 0
        error('Linkage cannot assemble at crank angle %.1f deg - check lengths.', phi(i));
    end
    % Tangent half-angle solution. "+" = open assembly;
    % use (B - sqrt(disc)) for the crossed assembly.
    t = (B + sqrt(disc)) / (A + C);
    psi(i) = 2 * atand(t);

    P2 = r2 * [cosd(phi(i)), sind(phi(i))];        % crank pin
    P3 = O4 + r4 * [cosd(psi(i)), sind(psi(i))];  % rocker pin
    M = (P2 + P3) / 2;                            % coupler midpoint
    cx(i) = M(1);
    cy(i) = M(2);

    % Transmission angle at P3: acute angle between coupler and rocker.
    u = P2 - P3;    % coupler direction at P3
    v = O4 - P3;    % rocker direction at P3 (toward its pivot)
    mu(i) = acosd(abs(dot(u, v)) / (norm(u) * norm(v)));
end

%% ------------------------------------------------------------------
% Report
% ------------------------------------------------------------------
swing = max(psi) - min(psi);
fprintf('--- Motion over one crank revolution ---\n');
fprintf('Rocker swing angle:      %.2f deg\n', swing);
fprintf('Transmission angle:      min %.1f deg, max %.1f deg\n', min(mu), max(mu));
if min(mu) < 40
    fprintf('WARNING: transmission angle < 40 deg -> poor force transmission.\n');
    fprintf('Consider lengthening the coupler or shortening the crank.\n');
end
fprintf('Coupler curve extent:    x [%.1f, %.1f] mm, y [%.1f, %.1f] mm\n\n', ...
    min(cx), max(cx), min(cy), max(cy));

%% ------------------------------------------------------------------
% Plots
% ------------------------------------------------------------------
figure('Name', 'Linkage positions and coupler curve');
hold on; axis equal; grid on;
plot(cx, cy, 'k-', 'LineWidth', 1.2);   % coupler curve
for a = [0, 90, 180, 270]
    P2 = r2 * [cosd(a), sind(a)];
    psia = interp1(phi, psi, a);
    P3 = O4 + r4 * [cosd(psia), sind(psia)];
    plot([O2(1), P2(1)], [O2(2), P2(2)], 'b-', 'LineWidth', 2);   % crank
    plot([P2(1), P3(1)], [P2(2), P3(2)], 'r-', 'LineWidth', 2);   % coupler
    plot([O4(1), P3(1)], [O4(2), P3(2)], 'g-', 'LineWidth', 2);   % rocker
end
plot([O2(1), O4(1)], [O2(2), O4(2)], 'ko-', 'LineWidth', 2.5, 'MarkerSize', 8);
xlabel('x (mm)'); ylabel('y (mm)');
legend('coupler curve', 'crank', 'coupler', 'rocker', 'ground', 'Location', 'best');
title('Clawbit four-bar: positions and coupler curve');

figure('Name', 'Rocker and transmission angle');
subplot(2, 1, 1);
plot(phi, psi, 'b-', 'LineWidth', 1.5); grid on;
xlabel('crank angle (deg)'); ylabel('rocker angle (deg)');
title('Rocker angle vs crank angle');
subplot(2, 1, 2);
plot(phi, mu, 'r-', 'LineWidth', 1.5); grid on; hold on;
line([0, 360], [40, 40], 'LineStyle', '--', 'Color', 'k');
xlabel('crank angle (deg)'); ylabel('transmission angle (deg)');
title('Transmission angle vs crank angle (dashed: 40 deg guideline)');
