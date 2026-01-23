/**
 * 碰撞检测工具类
 *
 * 功能：
 * 1. 检测两个游戏对象是否发生碰撞（矩形碰撞检测）
 * 2. 提供静态方法，无需实例化
 */

import { GameObject } from './GameObject';

export class CollisionDetector {
  /**
   * 检测两个游戏对象是否发生碰撞
   * 使用 AABB（轴对齐边界框）碰撞检测算法
   *
   * @param obj1 游戏对象 1
   * @param obj2 游戏对象 2
   * @returns 是否发生碰撞
   */
  static checkCollision(obj1: GameObject, obj2: GameObject): boolean {
    const bounds1 = obj1.getBounds();
    const bounds2 = obj2.getBounds();

    // AABB 碰撞检测：
    // 如果两个矩形在任意轴上没有重叠，则没有碰撞
    return !(
      bounds1.right < bounds2.left ||
      bounds1.left > bounds2.right ||
      bounds1.bottom < bounds2.top ||
      bounds1.top > bounds2.bottom
    );
  }

  /**
   * 检测一个对象与对象数组中的任意对象是否发生碰撞
   *
   * @param obj 游戏对象
   * @param objects 游戏对象数组
   * @returns 发生碰撞的对象，如果没有碰撞返回 null
   */
  static checkCollisionWithArray(
    obj: GameObject,
    objects: GameObject[]
  ): GameObject | null {
    for (const target of objects) {
      if (target.isAlive && this.checkCollision(obj, target)) {
        return target;
      }
    }
    return null;
  }

  /**
   * 检测一个对象数组与另一个对象数组之间的所有碰撞
   *
   * @param objects1 游戏对象数组 1
   * @param objects2 游戏对象数组 2
   * @returns 碰撞对数组 [obj1, obj2]
   */
  static checkAllCollisions(
    objects1: GameObject[],
    objects2: GameObject[]
  ): Array<[GameObject, GameObject]> {
    const collisions: Array<[GameObject, GameObject]> = [];

    for (const obj1 of objects1) {
      if (!obj1.isAlive) continue;

      for (const obj2 of objects2) {
        if (!obj2.isAlive) continue;

        if (this.checkCollision(obj1, obj2)) {
          collisions.push([obj1, obj2]);
        }
      }
    }

    return collisions;
  }
}
