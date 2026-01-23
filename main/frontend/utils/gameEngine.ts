/**
 * 游戏引擎核心逻辑
 *
 * 功能：
 * 1. 管理游戏循环（requestAnimationFrame）
 * 2. 管理游戏状态（未开始、进行中、暂停、结束）
 * 3. 管理所有游戏对象（玩家、敌机、子弹）
 * 4. 处理碰撞检测
 * 5. 管理分数和最高分
 * 6. 处理难度递增
 */

import { Player } from './Player';
import { Enemy, EnemyType } from './Enemy';
import { Bullet } from './Bullet';
import { CollisionDetector } from './CollisionDetector';

export enum GameState {
  NOT_STARTED = 'not_started',
  PLAYING = 'playing',
  PAUSED = 'paused',
  GAME_OVER = 'game_over',
}

export interface GameStats {
  score: number;
  highScore: number;
  enemiesDestroyed: number;
}

export class GameEngine {
  private canvas: HTMLCanvasElement;
  private ctx: CanvasRenderingContext2D;
  private state: GameState = GameState.NOT_STARTED;

  // 游戏对象
  private player: Player;
  private enemies: Enemy[] = [];
  private bullets: Bullet[] = [];

  // 游戏统计
  private score: number = 0;
  private highScore: number = 0;
  private enemiesDestroyed: number = 0;

  // 游戏计时器
  private lastBulletTime: number = 0;
  private lastEnemyTime: number = 0;
  private bulletInterval: number = 300; // 子弹发射间隔（毫秒）
  private enemyInterval: number = 1500; // 敌机生成间隔（毫秒）

  // 动画帧 ID
  private animationFrameId: number | null = null;

  // 键盘状态
  private keys: Set<string> = new Set();

  // 回调函数
  private onScoreChange?: (stats: GameStats) => void;
  private onGameOver?: (stats: GameStats) => void;

  constructor(canvas: HTMLCanvasElement) {
    this.canvas = canvas;
    const ctx = canvas.getContext('2d');
    if (!ctx) {
      throw new Error('无法获取 Canvas 2D 上下文');
    }
    this.ctx = ctx;

    // 初始化玩家
    this.player = new Player(canvas.width, canvas.height);

    // 加载最高分
    this.loadHighScore();

    // 绑定键盘事件
    this.bindKeyboardEvents();
  }

  /**
   * 设置回调函数
   */
  setCallbacks(callbacks: {
    onScoreChange?: (stats: GameStats) => void;
    onGameOver?: (stats: GameStats) => void;
  }): void {
    this.onScoreChange = callbacks.onScoreChange;
    this.onGameOver = callbacks.onGameOver;
  }

  /**
   * 开始游戏
   */
  start(): void {
    if (this.state === GameState.PLAYING) return;

    // 重置游戏状态
    this.score = 0;
    this.enemiesDestroyed = 0;
    this.enemies = [];
    this.bullets = [];
    this.player = new Player(this.canvas.width, this.canvas.height);
    this.lastBulletTime = Date.now();
    this.lastEnemyTime = Date.now();

    this.state = GameState.PLAYING;
    this.gameLoop();
  }

  /**
   * 暂停游戏
   */
  pause(): void {
    if (this.state === GameState.PLAYING) {
      this.state = GameState.PAUSED;
    }
  }

  /**
   * 继续游戏
   */
  resume(): void {
    if (this.state === GameState.PAUSED) {
      this.state = GameState.PLAYING;
      this.gameLoop();
    }
  }

  /**
   * 游戏主循环
   */
  private gameLoop = (): void => {
    if (this.state !== GameState.PLAYING) return;

    // 更新游戏逻辑
    this.update();

    // 渲染游戏画面
    this.render();

    // 请求下一帧
    this.animationFrameId = requestAnimationFrame(this.gameLoop);
  };

  /**
   * 更新游戏逻辑
   */
  private update(): void {
    const now = Date.now();

    // 处理玩家移动
    this.updatePlayerMovement();

    // 自动发射子弹
    if (now - this.lastBulletTime > this.bulletInterval) {
      this.shootBullet();
      this.lastBulletTime = now;
    }

    // 生成敌机
    if (now - this.lastEnemyTime > this.enemyInterval) {
      this.spawnEnemy();
      this.lastEnemyTime = now;
    }

    // 更新所有游戏对象
    this.bullets.forEach(bullet => bullet.update());
    this.enemies.forEach(enemy => enemy.update());

    // 移除飞出边界的对象
    this.bullets = this.bullets.filter(bullet => !bullet.isOutOfBounds());
    this.enemies = this.enemies.filter(enemy => !enemy.isOutOfBounds(this.canvas.height));

    // 碰撞检测
    this.checkCollisions();

    // 难度递增
    this.updateDifficulty();
  }

  /**
   * 更新玩家移动
   */
  private updatePlayerMovement(): void {
    if (this.keys.has('ArrowLeft')) {
      this.player.moveLeft();
    }
    if (this.keys.has('ArrowRight')) {
      this.player.moveRight();
    }
  }

  /**
   * 发射子弹
   */
  private shootBullet(): void {
    const pos = this.player.getBulletSpawnPosition();
    const bullet = new Bullet(pos.x, pos.y);
    this.bullets.push(bullet);
  }

  /**
   * 生成敌机
   */
  private spawnEnemy(): void {
    const enemy = Enemy.createRandom(this.canvas.width);
    this.enemies.push(enemy);
  }

  /**
   * 碰撞检测
   */
  private checkCollisions(): void {
    // 子弹与敌机碰撞
    const bulletEnemyCollisions = CollisionDetector.checkAllCollisions(this.bullets, this.enemies);
    bulletEnemyCollisions.forEach(([bullet, enemy]) => {
      bullet.destroy();
      enemy.destroy();
      this.addScore((enemy as Enemy).score);
      this.enemiesDestroyed++;
    });

    // 移除被销毁的对象
    this.bullets = this.bullets.filter(bullet => bullet.isAlive);
    this.enemies = this.enemies.filter(enemy => enemy.isAlive);

    // 玩家与敌机碰撞
    const playerCollision = CollisionDetector.checkCollisionWithArray(this.player, this.enemies);
    if (playerCollision) {
      this.gameOver();
    }
  }

  /**
   * 增加分数
   */
  private addScore(points: number): void {
    this.score += points;

    // 更新最高分
    if (this.score > this.highScore) {
      this.highScore = this.score;
      this.saveHighScore();
    }

    // 触发回调
    if (this.onScoreChange) {
      this.onScoreChange(this.getStats());
    }
  }

  /**
   * 难度递增
   * 每得 100 分，敌机生成频率增加 10%
   */
  private updateDifficulty(): void {
    const level = Math.floor(this.score / 100);
    const minInterval = 500; // 最小间隔 0.5 秒
    this.enemyInterval = Math.max(minInterval, 1500 - level * 150);
  }

  /**
   * 游戏结束
   */
  private gameOver(): void {
    this.state = GameState.GAME_OVER;

    if (this.animationFrameId) {
      cancelAnimationFrame(this.animationFrameId);
      this.animationFrameId = null;
    }

    // 触发回调
    if (this.onGameOver) {
      this.onGameOver(this.getStats());
    }
  }

  /**
   * 渲染游戏画面
   */
  private render(): void {
    // 清空画布
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

    // 绘制背景（蓝天渐变）
    const gradient = this.ctx.createLinearGradient(0, 0, 0, this.canvas.height);
    gradient.addColorStop(0, '#87CEEB'); // 天蓝色
    gradient.addColorStop(1, '#E0F6FF'); // 浅蓝色
    this.ctx.fillStyle = gradient;
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

    // 绘制白云（简单装饰）
    this.drawClouds();

    // 渲染游戏对象
    this.player.render(this.ctx);
    this.bullets.forEach(bullet => bullet.render(this.ctx));
    this.enemies.forEach(enemy => enemy.render(this.ctx));
  }

  /**
   * 绘制白云装饰
   */
  private drawClouds(): void {
    this.ctx.fillStyle = 'rgba(255, 255, 255, 0.6)';

    // 绘制几朵简单的云
    const clouds = [
      { x: 100, y: 80 },
      { x: 400, y: 150 },
      { x: 650, y: 100 },
    ];

    clouds.forEach(cloud => {
      this.ctx.beginPath();
      this.ctx.arc(cloud.x, cloud.y, 30, 0, Math.PI * 2);
      this.ctx.arc(cloud.x + 25, cloud.y, 35, 0, Math.PI * 2);
      this.ctx.arc(cloud.x + 50, cloud.y, 30, 0, Math.PI * 2);
      this.ctx.fill();
    });
  }

  /**
   * 绑定键盘事件
   */
  private bindKeyboardEvents(): void {
    window.addEventListener('keydown', (e) => {
      if (['ArrowLeft', 'ArrowRight'].includes(e.key)) {
        e.preventDefault();
        this.keys.add(e.key);
      }
    });

    window.addEventListener('keyup', (e) => {
      this.keys.delete(e.key);
    });
  }

  /**
   * 处理鼠标移动（鼠标控制飞机）
   */
  handleMouseMove(x: number): void {
    if (this.state === GameState.PLAYING) {
      this.player.moveTo(x);
    }
  }

  /**
   * 获取游戏统计信息
   */
  getStats(): GameStats {
    return {
      score: this.score,
      highScore: this.highScore,
      enemiesDestroyed: this.enemiesDestroyed,
    };
  }

  /**
   * 获取游戏状态
   */
  getState(): GameState {
    return this.state;
  }

  /**
   * 保存最高分到 localStorage
   */
  private saveHighScore(): void {
    try {
      localStorage.setItem('planeGameHighScore', this.highScore.toString());
    } catch (error) {
      console.error('保存最高分失败:', error);
    }
  }

  /**
   * 从 localStorage 加载最高分
   */
  private loadHighScore(): void {
    try {
      const saved = localStorage.getItem('planeGameHighScore');
      if (saved) {
        this.highScore = parseInt(saved, 10) || 0;
      }
    } catch (error) {
      console.error('加载最高分失败:', error);
    }
  }

  /**
   * 销毁游戏引擎
   */
  destroy(): void {
    if (this.animationFrameId) {
      cancelAnimationFrame(this.animationFrameId);
    }
    this.keys.clear();
  }
}
